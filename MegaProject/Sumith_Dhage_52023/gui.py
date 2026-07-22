from datetime import datetime
from tkinter import messagebox
import time
import customtkinter as ctk
from config import GRAPH_REFRESH_MS, LOG_FILE, PHYSICS_STEP_SECONDS, PHYSICS_TIMER_MS, TELEMETRY_REFRESH_MS
from data_logger import ExcelDataLogger
from graph_manager import VelocityGraphManager
from vehicle_dynamics import PhysicsResult, VehicleState, calculate_vehicle_motion, determine_operating_state, update_pedals

class CarEmulatorApplication(ctk.CTk):
    BG, PANEL, CARD = "#07131F", "#0D1B2A", "#12263A"
    WHITE, GREY, GREEN = "#E2E8F0", "#94A3B8", "#22C55E"
    BLUE, RED, ORANGE = "#06B6D4", "#EF4444", "#F59E0B"

    def __init__(self):
        super().__init__() # Inherit the parent's methods
        ctk.set_appearance_mode("dark")            # set dark theme
        ctk.set_default_color_theme("dark-blue")   # set application theme as dark
        self.title("Car Emulator GUI & Vehicle Motion Simulator") # Adding title to the GUI application interface (Self because it is inherited from the CTK library)
        self.geometry("1280X740") # width X Height in pixels
        self.minsize(1080, 650) # minimum size of the window (Even after the split screen)
        self.configure(fg_color=self.BG) # foregrtound color same as background color for dark theme
        self.active = self.stop_requested = self.save_pending = False # simulation running? Is stop button pressed ? any pending save option?
        self.accel_held = self.brake_held = False # initial state of accelerator and brake pedals
        self.vehicle_state = VehicleState() 
        self.result = PhysicsResult(*([0.0] * 9))
        self.physics_job = self.telemetry_job = self.graph_job = None
        self.session_id, self.session_start = 0, None
        self.stop_time = self.stop_speed = None
        self.records, self.accumulator = [], 0.0
        self.last_clock = time.perf_counter()
        self.logger = ExcelDataLogger()
        self.build_gui()
        self.bind_pedals()
        self.update_display()
        self.protocol("WM_DELETE_WINDOW", self.close_application)

    def build_gui(self):
        header = ctk.CTkFrame(self, fg_color=self.PANEL, corner_radius=0, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="CAR EMULATOR GUI & VEHICLE MOTION SIMULATOR", font=("Arial", 25, "bold"), text_color=self.WHITE).pack(side="left", padx=24)
        self.session_label = ctk.CTkLabel(header, text="SESSION: READY", font=("Consolas", 13, "bold"), text_color=self.BLUE)
        self.session_label.pack(side="right", padx=24)
        main = ctk.CTkFrame(self, fg_color=self.BG)
        main.pack(fill="both", expand=True, padx=18, pady=18)
        main.grid_columnconfigure(0, minsize=410)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)
        left = ctk.CTkFrame(main, fg_color=self.PANEL, corner_radius=16)
        right = ctk.CTkFrame(main, fg_color=self.PANEL, corner_radius=16)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right.grid(row=0, column=1, sticky="nsew")
        self.build_controls(left)
        self.build_graph(right)

    def build_controls(self, parent):
        ctk.CTkLabel(parent, text="LIVE TELEMETRY", font=("Arial", 16, "bold"), text_color=self.GREY).pack(anchor="w", padx=20, pady=(18, 8))
        card = ctk.CTkFrame(parent, fg_color=self.CARD, corner_radius=14)
        card.pack(fill="x", padx=18, pady=8)
        self.speed_label = ctk.CTkLabel(card, text="0.0", font=("Consolas", 54, "bold"), text_color=self.GREEN)
        self.speed_label.pack(pady=(14, 0))
        ctk.CTkLabel(card, text="km/h", text_color=self.GREY).pack(pady=(0, 12))
        metrics = ctk.CTkFrame(parent, fg_color="transparent")
        metrics.pack(fill="x", padx=18, pady=6)
        metrics.grid_columnconfigure((0, 1), weight=1)
        data = [("ACCELERATOR", self.BLUE, 0, 0), ("BRAKE", self.RED, 0, 1), ("ACCELERATION", self.ORANGE, 1, 0), ("STATE", self.WHITE, 1, 1)]
        self.accel_label, self.brake_label, self.acceleration_label, self.state_label = [self.make_metric(metrics, *item) for item in data]
        self.accel_bar = ctk.CTkProgressBar(parent, progress_color=self.BLUE)
        self.brake_bar = ctk.CTkProgressBar(parent, progress_color=self.RED)
        self.accel_bar.pack(fill="x", padx=20, pady=(8, 4))
        self.brake_bar.pack(fill="x", padx=20, pady=(4, 12))
        buttons = ctk.CTkFrame(parent, fg_color="transparent")
        buttons.pack(fill="x", padx=18, pady=8)
        buttons.grid_columnconfigure((0, 1), weight=1)
        self.start_button = self.make_button(buttons, "START", "#15803D", 0, 0, self.start_session)
        self.stop_button = self.make_button(buttons, "STOP", "#B91C1C", 0, 1, self.stop_session)
        self.accel_button = self.make_button(buttons, "HOLD ACCELERATOR", "#0369A1", 1, 0, height=64)
        self.brake_button = self.make_button(buttons, "HOLD BRAKE", "#C2410C", 1, 1, height=64)
        ctk.CTkLabel(parent, text="Physics: 5 ms | STOP coasts | START resumes", text_color=self.GREY).pack(anchor="w", padx=22, pady=(8, 16))

    def build_graph(self, parent):
        ctk.CTkLabel(parent, text="REAL-TIME VELOCITY-TIME GRAPH", font=("Arial", 16, "bold"), text_color=self.GREY).pack(anchor="w", padx=20, pady=(18, 6))
        self.graph = VelocityGraphManager(parent)
        

    def make_metric(self, parent, title, color, row, column):
        card = ctk.CTkFrame(parent, fg_color=self.CARD, corner_radius=10)
        card.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(card, text=title, font=("Arial", 10, "bold"), text_color=self.GREY).pack(pady=(8, 1))
        label = ctk.CTkLabel(card, text="0.0", font=("Consolas", 15, "bold"), text_color=color)
        label.pack(pady=(0, 8))
        return label

    def make_button(self, parent, text, color, row, column, command=None, height=48):
        button = ctk.CTkButton(parent, text=text, height=height, fg_color=color, command=command)
        button.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        return button

    def bind_pedals(self):
        for button, setter in ((self.accel_button, self.set_accelerator), (self.brake_button, self.set_brake)):
            button.bind("<ButtonPress-1>", lambda event, function=setter: function(True))
            button.bind("<ButtonRelease-1>", lambda event, function=setter: function(False))
            button.bind("<Leave>", lambda event, function=setter: function(False))

    def set_accelerator(self, held):
        if self.active and not self.stop_requested:
            self.accel_held = held
            if held:
                self.brake_held = False

    def set_brake(self, held):
        if self.active and not self.save_pending:
            self.brake_held = held
            if held:
                self.accel_held = False

    def start_session(self):
        if self.active:
            if self.stop_requested and not self.save_pending:
                self.stop_requested = False
                self.stop_time = self.stop_speed = None
                self.accel_held = self.brake_held = False
                self.vehicle_state.operating_state = determine_operating_state(self.vehicle_state)
                self.reset_clock()
                self.update_display()
            return
        self.active, self.stop_requested, self.save_pending = True, False, False
        self.accel_held = self.brake_held = False
        self.vehicle_state = VehicleState(operating_state="STATIONARY")
        self.result = PhysicsResult(*([0.0] * 9))
        self.session_id = self.logger.get_next_session_id()
        self.session_start = datetime.now()
        self.stop_time = self.stop_speed = None
        self.records = []
        self.graph.reset()
        self.reset_clock()
        self.update_display()
        self.start_jobs()

    def reset_clock(self):
        self.last_clock = time.perf_counter()
        self.accumulator = 0.0

    def start_jobs(self):
        self.physics_job = self.after(PHYSICS_TIMER_MS, self.physics_loop)
        self.telemetry_job = self.after(TELEMETRY_REFRESH_MS, self.telemetry_loop)
        self.graph_job = self.after(GRAPH_REFRESH_MS, self.graph_loop)

    def physics_loop(self):
        if not self.active or self.save_pending:
            return
        current_time = time.perf_counter()
        self.accumulator += current_time - self.last_clock
        self.last_clock = current_time
        for _ in range(min(int(self.accumulator / PHYSICS_STEP_SECONDS), 20)):
            self.physics_step()
            self.accumulator -= PHYSICS_STEP_SECONDS
            if not self.active or self.save_pending:
                break
        if self.active and not self.save_pending:
            self.physics_job = self.after(PHYSICS_TIMER_MS, self.physics_loop)

    def physics_step(self):
        state = self.vehicle_state
        update_pedals(state, self.accel_held, self.brake_held, PHYSICS_STEP_SECONDS)
        self.result = calculate_vehicle_motion(state, PHYSICS_STEP_SECONDS)
        state.vehicle_speed_kmh = self.result.speed_kmh
        state.vehicle_acceleration_m_s2 = self.result.acceleration_m_s2
        state.elapsed_time_seconds = round(state.elapsed_time_seconds + PHYSICS_STEP_SECONDS, 6)
        state.operating_state = ("POST-STOP BRAKING" if state.brake_percentage > 0.5 else "POST-STOP COASTING") if self.stop_requested else determine_operating_state(state)
        self.graph.add_sample(state.elapsed_time_seconds, state.vehicle_speed_kmh)
        self.records.append(self.logger.make_record(self.session_id, state, self.result, len(self.records) + 1))
        if self.stop_requested and state.vehicle_speed_kmh == 0:
            self.finish_session()

    def telemetry_loop(self):
        if not self.active or self.save_pending:
            return
        self.update_display()
        self.telemetry_job = self.after(TELEMETRY_REFRESH_MS, self.telemetry_loop)

    def graph_loop(self):
        if not self.active or self.save_pending:
            return
        self.graph.draw()
        self.graph_job = self.after(GRAPH_REFRESH_MS, self.graph_loop)

    def stop_session(self):
        if self.save_pending:
            self.finish_session()
            return
        if not self.active or self.stop_requested:
            return
        self.stop_requested = True
        self.stop_time = self.vehicle_state.elapsed_time_seconds
        self.stop_speed = self.vehicle_state.vehicle_speed_kmh
        self.accel_held = False
        self.vehicle_state.accelerator_percentage = 0.0
        self.vehicle_state.operating_state = "POST-STOP COASTING"
        self.update_display()
        if self.vehicle_state.vehicle_speed_kmh == 0:
            self.finish_session()

    def finish_session(self):
        self.cancel_jobs()
        self.save_pending = True
        self.update_display()
        try:
            summary = self.logger.make_summary(self.session_id, self.session_start, self.vehicle_state, self.stop_time, self.stop_speed, self.records)
            self.logger.save_session(summary, self.records)
        except Exception as error:
            messagebox.showerror("Save failed", str(error))
            return
        self.graph.add_final_zero(self.vehicle_state.elapsed_time_seconds)
        self.vehicle_state = VehicleState(operating_state="STOPPED")
        self.active = self.stop_requested = self.save_pending = False
        self.accel_held = self.brake_held = False
        self.update_display()
        messagebox.showinfo("Session saved", f"Session {self.session_id} saved to:\n{LOG_FILE}")

    def update_display(self):
        state = self.vehicle_state
        start_available = not self.active or (self.stop_requested and not self.save_pending)
        self.start_button.configure(state="normal" if start_available else "disabled", text="RESTART" if self.stop_requested and not self.save_pending else "START")
        self.accel_button.configure(state="normal" if self.active and not self.stop_requested else "disabled")
        self.brake_button.configure(state="normal" if self.active and not self.save_pending else "disabled")
        stop_available = (self.active and not self.stop_requested) or self.save_pending
        self.stop_button.configure(state="normal" if stop_available else "disabled", text="RETRY SAVE" if self.save_pending else "STOP")
        self.speed_label.configure(text=f"{state.vehicle_speed_kmh:.1f}")
        self.accel_label.configure(text=f"{state.accelerator_percentage:.1f} %")
        self.brake_label.configure(text=f"{state.brake_percentage:.1f} %")
        self.acceleration_label.configure(text=f"{state.vehicle_acceleration_m_s2:.2f} m/s²")
        self.state_label.configure(text=state.operating_state)
        self.accel_bar.set(state.accelerator_percentage / 100)
        self.brake_bar.set(state.brake_percentage / 100)
        phase = "STOPPING" if self.stop_requested else "RUNNING"
        text = f"SESSION {self.session_id} | {phase} | {state.elapsed_time_seconds:.3f} s" if self.active else "SESSION: READY"
        self.session_label.configure(text=text)

    def cancel_jobs(self):
        for name in ("physics_job", "telemetry_job", "graph_job"):
            job = getattr(self, name)
            if job:
                self.after_cancel(job)
                setattr(self, name, None)

    def close_application(self):
        if self.active and not messagebox.askyesno("Exit", "The active session will not be saved. Exit?"):
            return
        self.cancel_jobs()
        self.destroy()
