#!/usr/bin/env python3
"""
Accel-Easing: standalone PyQt6 + pyqtgraph simulator

Run:
    python3 main.py
"""

from collections import deque
import sys
import numpy as np
import inertial_body_py as ib

from PyQt6 import QtCore, QtWidgets
import pyqtgraph as pg


class SpringSimulator(QtCore.QObject):
    """Physics state + stepping logic for a damped spring towards a target."""

    updated = QtCore.pyqtSignal(float, float, float)  # emits pos, vel, accel each step

    def __init__(self, k=1, c=0.2, mass=0.01, target=1, de=0, dt=0.01):
        super().__init__()
        self.elasticity = float(k)
        self.friction = float(c)
        self.mass = float(mass)
        self.target = int(target)
        self.dt = float(dt)
        self.distance_exponent = float(de)

        self.pos = 0.0
        self.vel = 0.0

        # option to pause internal stepping (controller handles running)
        self._running = False

    def reset(self, pos=0.0, vel=0.0):
        self.pos = float(pos)
        self.vel = float(vel)

    def step(self):
        """Single physics step (explicit Euler)."""
        # distance
        d = self.target - self.pos

        # normalize distance exponent
        p = min(max(self.distance_exponent, -1), 1) + 1

        spring = self.elasticity * np.sign(d) * abs(d) ** p
        damping = - self.friction * self.vel

        # acceleration = total force / mass
        accel = (spring + damping) / self.mass

        # integrate
        self.vel += accel * self.dt
        self.pos += self.vel * self.dt

        # emit new state
        self.updated.emit(self.pos, self.vel, accel)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accel-Easing Simulator (PyQt6 + pyqtgraph)")
        self.resize(1000, 700)

        # default simulation parameters
        self.dt = 0.01  # seconds per physics step
        self.sim = SpringSimulator(dt=self.dt)
        self._draw_every_n = 1 

        # Data history (use deque for efficient append/pop)
        self.max_history = 8000
        self.pos_hist = deque(maxlen=self.max_history)
        self.target_hist = deque(maxlen=self.max_history)
        self.vel_hist = deque(maxlen=self.max_history)
        self.acc_hist = deque(maxlen=self.max_history)
        self.time_hist = deque(maxlen=self.max_history)
        self.step_counter = 0

        self._setup_ui()
        self._connect_signals()

        # QTimer for stepping simulation; runs in UI thread but non-blocking.
        self.timer = QtCore.QTimer(self)
        fps = 120
        self.timer.setInterval(int(self.dt * 1000 * (1/fps)))  #  milliseconds
        self.timer.timeout.connect(self._on_timer)

        # redraw throttle (so plots don't update every single step)
        self._draw_every_n = 2
        self._draw_counter = 0

    def _setup_ui(self):
        # central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # Left: controls
        ctrl_widget = QtWidgets.QWidget()
        ctrl_layout = QtWidgets.QFormLayout(ctrl_widget)

        # k (spring constant)
        self.k_spin = QtWidgets.QDoubleSpinBox()
        self.k_spin.setRange(0.01, 1)
        self.k_spin.setSingleStep(0.01)
        self.k_spin.setValue(self.sim.elasticity)
        ctrl_layout.addRow("elasticity", self.k_spin)

        # c (damping/friction)
        self.c_spin = QtWidgets.QDoubleSpinBox()
        self.c_spin.setRange(0.01, 1)
        self.c_spin.setSingleStep(0.01)
        self.c_spin.setValue(self.sim.friction)
        ctrl_layout.addRow("friction", self.c_spin)

        # mass
        self.m_spin = QtWidgets.QDoubleSpinBox()
        self.k_spin.setRange(0.01, 1)
        self.m_spin.setSingleStep(0.01)
        self.m_spin.setValue(self.sim.mass)
        ctrl_layout.addRow("mass", self.m_spin)

        # target
        self.target_spin = QtWidgets.QDoubleSpinBox()
        self.target_spin.setRange(0, 1)
        self.target_spin.setSingleStep(0.1)
        self.target_spin.setValue(self.sim.target)
        ctrl_layout.addRow("target", self.target_spin)

        # distance exponent
        self.de_spin = QtWidgets.QDoubleSpinBox()
        self.de_spin.setRange(-1, 1)
        self.de_spin.setSingleStep(0.1)
        self.de_spin.setValue(self.sim.distance_exponent)
        ctrl_layout.addRow("distance exponent (-1 to 1)", self.de_spin)

        # control buttons
        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setCheckable(True)
        self.reset_btn = QtWidgets.QPushButton("Reset")
        btn_h = QtWidgets.QHBoxLayout()
        btn_h.addWidget(self.start_btn)
        btn_h.addWidget(self.reset_btn)
        ctrl_layout.addRow(btn_h)

        # extra controls
        self.history_spin = QtWidgets.QSpinBox()
        self.history_spin.setRange(100, 20000)
        self.history_spin.setValue(8000)
        ctrl_layout.addRow("History length", self.history_spin)

        self.drawrate_spin = QtWidgets.QSpinBox()
        self.drawrate_spin.setRange(1, 50)
        self.drawrate_spin.setValue(self._draw_every_n)
        ctrl_layout.addRow("Plot update every N steps", self.drawrate_spin)

        ctrl_layout.addRow("dt (s)", QtWidgets.QLabel(f"{self.dt:.4f}"))

        # Right: plots (vertical)
        plot_widget = QtWidgets.QWidget()
        plot_layout = QtWidgets.QVBoxLayout(plot_widget)

        pg.setConfigOptions(antialias=True)  # nicer lines

        self.plot_pos = pg.PlotWidget(title="Position")
        self.plot_vel = pg.PlotWidget(title="Velocity")
        self.plot_acc = pg.PlotWidget(title="Acceleration")

        # set labels
        self.plot_pos.setLabel('left', 'Position')
        self.plot_vel.setLabel('left', 'Velocity')
        self.plot_acc.setLabel('left', 'Acceleration')
        self.plot_acc.setLabel('bottom', 'Steps')

        # add curves
        self.curve_pos = self.plot_pos.plot([], [], pen=pg.mkPen(width=2))
        self.curve_target = self.plot_pos.plot(
            [], [], pen=pg.mkPen(color=(100, 100, 200), width=2, style=QtCore.Qt.PenStyle.DashLine),name="Target"
        )
        self.curve_vel = self.plot_vel.plot([], [], pen=pg.mkPen(width=2))
        self.curve_acc = self.plot_acc.plot([], [], pen=pg.mkPen(width=2))

        # pack plots
        plot_layout.addWidget(self.plot_pos)
        plot_layout.addWidget(self.plot_vel)
        plot_layout.addWidget(self.plot_acc)

        layout.addWidget(ctrl_widget, 0)
        layout.addWidget(plot_widget, 1)

        # status bar
        self.status = self.statusBar()
        self._update_status("Ready")

    def _connect_signals(self):
        # UI -> simulator params
        self.k_spin.valueChanged.connect(lambda v: setattr(self.sim, "k", float(v)))
        self.c_spin.valueChanged.connect(lambda v: setattr(self.sim, "c", float(v)))
        self.m_spin.valueChanged.connect(lambda v: setattr(self.sim, "mass", float(v)))
        self.target_spin.valueChanged.connect(lambda v: setattr(self.sim, "target", float(v)))

        # control buttons
        self.start_btn.toggled.connect(self._on_start_toggled)
        self.reset_btn.clicked.connect(self._on_reset)

        # internal simulator update -> collect data
        self.sim.updated.connect(self._on_sim_updated)

        # additional UI
        self.history_spin.valueChanged.connect(self._on_history_changed)
        self.drawrate_spin.valueChanged.connect(lambda v: setattr(self, "_draw_every_n", int(v)))

    def _on_start_toggled(self, checked):
        if checked:
            self.start_btn.setText("Stop")
            self.timer.start()
            self._update_status("Running")
        else:
            self.start_btn.setText("Start")
            self.timer.stop()
            self._update_status("Stopped")

    def _on_reset(self):
        # reset simulation state and buffers
        self.sim.reset(pos=0.0, vel=0.0)
        self.pos_hist.clear()
        self.vel_hist.clear()
        self.acc_hist.clear()
        self.time_hist.clear()
        self.target_hist.clear()
        self.step_counter = 0
        # clear plots
        self.curve_pos.setData([], [])
        self.curve_vel.setData([], [])
        self.curve_acc.setData([], [])
        self._update_status("Reset")

    def _on_history_changed(self, val):
        self.max_history = int(val)
        # re-create deques with new length preserving existing data
        self.pos_hist = deque(list(self.pos_hist), maxlen=self.max_history)
        self.vel_hist = deque(list(self.vel_hist), maxlen=self.max_history)
        self.acc_hist = deque(list(self.acc_hist), maxlen=self.max_history)
        self.time_hist = deque(list(self.time_hist), maxlen=self.max_history)
        self.target_hist = deque(list(self.target_hist), maxlen=self.max_history)

    def _on_timer(self):
        # perform one or more physics steps per timer tick if desired
        # Here we perform exactly one step per tick (dt)
        self.sim.step()

    def _on_sim_updated(self, pos, vel, accel):
        # Append history
        self.pos_hist.append(pos)
        self.target_hist.append(self.sim.target)
        self.vel_hist.append(vel)
        self.acc_hist.append(accel)
        self.time_hist.append(self.step_counter)
        self.step_counter += 1

        # throttle plotting to reduce UI overhead
        self._draw_counter += 1
        if self._draw_counter >= self._draw_every_n:
            self._draw_counter = 0
            self._update_plots()

    def _update_plots(self):
        x = np.array(self.time_hist)
        pos = np.array(self.pos_hist)
        vel = np.array(self.vel_hist)
        acc = np.array(self.acc_hist)
        tar = np.array(self.target_hist)

        if x.size == 0:
            return

        self.curve_pos.setData(x, pos)
        self.curve_target.setData(x, tar)
        self.curve_vel.setData(x, vel)
        self.curve_acc.setData(x, acc)

        # auto-range Y for each plot to keep things visible (with padding)
        for arr, plot in ((pos, self.plot_pos), (vel, self.plot_vel), (acc, self.plot_acc)):
            if arr.size > 0:
                vmin, vmax = float(np.min(arr)), float(np.max(arr))
                if vmin == vmax:
                    vmin -= 1.0
                    vmax += 1.0
                padding = (vmax - vmin) * 0.15
                plot.setYRange(vmin - padding, vmax + padding, padding=0)

        # set x range to show last N samples
        N = min(len(x), 500)
        self.plot_pos.setXRange(x[-N], x[-1])
        self.plot_vel.setXRange(x[-N], x[-1])
        self.plot_acc.setXRange(x[-N], x[-1])

    def _update_status(self, text: str):
        self.status.showMessage(text, 4000)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
