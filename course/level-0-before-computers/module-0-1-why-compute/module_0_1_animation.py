"""
Module 0.1 — Why Did Humans Need to Compute?
A presentation-style faceless animated video built with Manim Community Edition.

Render commands:
  Direct Python run (Preview):
    python module_0_1_animation.py
  High Quality (1080p 60fps):
    python -m manim -pqh module_0_1_animation.py WhyComputeScene
  Production 4K (3840x2160 60fps):
    python -m manim -pqk -r 3840,2160 module_0_1_animation.py WhyComputeScene
"""

import os
import sys
import unittest.mock

# Ensure ffmpeg from winget is in system PATH
FFMPEG_BIN = r"C:\Users\ssro2\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
if os.path.exists(FFMPEG_BIN) and FFMPEG_BIN not in os.environ["PATH"]:
    os.environ["PATH"] = FFMPEG_BIN + os.pathsep + os.environ["PATH"]

# Bypass Windows Application Control block on optional PyAV wheel
for mod in ["av", "av.audio", "av.audio.stream", "av.audio.codeccontext"]:
    if mod not in sys.modules:
        sys.modules[mod] = unittest.mock.MagicMock()

from manim import *
import manim.utils.file_ops
import manim.scene.scene_file_writer
import time
import subprocess
from pathlib import Path

def safe_modify_atime(file_path):
    try:
        p = Path(file_path)
        if p.exists():
            os.utime(file_path, times=(time.time(), p.stat().st_mtime))
    except Exception:
        pass

class FFmpegPartialMovieEncodeJob:
    def __init__(self, path, animation_index, width, height, fps):
        self.path = str(path)
        self.animation_index = animation_index
        ffmpeg_exec = os.path.join(FFMPEG_BIN, "ffmpeg.exe") if os.path.exists(os.path.join(FFMPEG_BIN, "ffmpeg.exe")) else "ffmpeg"
        cmd = [
            ffmpeg_exec, "-y",
            "-f", "rawvideo",
            "-s", f"{width}x{height}",
            "-pix_fmt", "rgba",
            "-r", str(fps),
            "-i", "-",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            self.path
        ]
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.failed = False

    def put(self, num_frames, frame):
        raw = frame.tobytes()
        for _ in range(num_frames):
            try:
                self.proc.stdin.write(raw)
            except Exception:
                self.failed = True
                break

    def seal(self):
        if self.proc.stdin and not self.proc.stdin.closed:
            try:
                self.proc.stdin.close()
            except Exception:
                pass

    def join(self):
        self.seal()
        self.proc.wait()

def open_partial_movie_stream(self, file_path=None):
    if file_path is None:
        file_path = self.partial_movie_files[self.renderer.num_plays]
    self.partial_movie_file_path = file_path
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    self._current_encode_job = FFmpegPartialMovieEncodeJob(
        file_path,
        self.renderer.num_plays,
        config.pixel_width,
        config.pixel_height,
        config.frame_rate
    )

def ffmpeg_combine_files(self, input_files, output_file, create_gif=False, includes_sound=False):
    file_list = self.partial_movie_directory / "partial_movie_file_list.txt"
    with file_list.open("w", encoding="utf-8") as fp:
        for pf in input_files:
            abs_p = Path(pf).resolve().as_posix()
            fp.write(f"file '{abs_p}'\n")

    ffmpeg_exec = os.path.join(FFMPEG_BIN, "ffmpeg.exe") if os.path.exists(os.path.join(FFMPEG_BIN, "ffmpeg.exe")) else "ffmpeg"
    cmd = [
        ffmpeg_exec, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(file_list),
        "-c", "copy",
        str(output_file)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

manim.utils.file_ops.modify_atime = safe_modify_atime
manim.scene.scene_file_writer.modify_atime = safe_modify_atime
manim.scene.scene_file_writer.SceneFileWriter.open_partial_movie_stream = open_partial_movie_stream
manim.scene.scene_file_writer.SceneFileWriter.combine_files = ffmpeg_combine_files

class WhyComputeScene(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Palette & Style System
        # ---------------------------------------------------------
        BG_COLOR = "#0A0E17"
        CARD_BG = "#131B2E"
        ACCENT_CYAN = "#38BDF8"
        ACCENT_AMBER = "#F59E0B"
        ACCENT_RED = "#EF4444"
        ACCENT_GREEN = "#10B981"
        ACCENT_PURPLE = "#A855F7"
        TEXT_PRIMARY = "#F8FAFC"
        TEXT_MUTED = "#94A3B8"
        BORDER_COLOR = "#1E293B"

        self.camera.background_color = BG_COLOR

        # Helper method for consistent rounded card containers
        def create_card(width, height, stroke_color=BORDER_COLOR, fill_color=CARD_BG, fill_opacity=0.88):
            return RoundedRectangle(
                corner_radius=0.2,
                width=width,
                height=height,
                stroke_color=stroke_color,
                stroke_width=2,
                fill_color=fill_color,
                fill_opacity=fill_opacity
            )

        # =========================================================
        # ACT 1: TITLE & THE 1880 CENSUS CRISIS
        # =========================================================
        tag = RoundedRectangle(
            corner_radius=0.12, width=3.4, height=0.55,
            fill_color="#1E293B", fill_opacity=0.9, stroke_color=ACCENT_CYAN, stroke_width=1.5
        )
        tag_text = Text("MODULE 0.1 // FOUNDATIONS", font_size=15, color=ACCENT_CYAN, weight=BOLD)
        tag_group = VGroup(tag, tag_text).to_edge(UP, buff=0.8)

        title = Text("Why Did Humans Need to Compute?", font_size=38, weight=BOLD, color=TEXT_PRIMARY)
        title.next_to(tag_group, DOWN, buff=0.35)

        subtitle = Text("The Failure of Human Scale & The Birth of Machines", font_size=20, color=TEXT_MUTED)
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(tag_group, shift=DOWN * 0.3), Write(title), run_time=1.4)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.9)
        self.wait(2.2)

        # Transition to Census Crisis
        self.play(
            FadeOut(tag_group, shift=UP * 0.5),
            FadeOut(subtitle, shift=DOWN * 0.3),
            title.animate.scale(0.65).to_corner(UL, buff=0.6).set_color(ACCENT_CYAN),
            run_time=1.0
        )

        # Section Banner: Census
        sec1_badge = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_AMBER, stroke_width=1.5)
        sec1_badge_lbl = Text("CASE 1: THE 1880 US CENSUS", font_size=15, color=ACCENT_AMBER, weight=BOLD)
        sec1_group = VGroup(sec1_badge, sec1_badge_lbl).to_edge(UP, buff=0.6)
        self.play(FadeIn(sec1_group, shift=DOWN * 0.2))

        # Census Infographic Cards (Left: Scale, Right: Timeline Crisis)
        card_left = create_card(5.6, 4.4)
        card_left.shift(LEFT * 3.3 + DOWN * 0.4)

        pop_title = Text("POPULATION COUNT", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(card_left.get_top() + DOWN * 0.45)
        pop_num = Text("50,155,783", font_size=34, color=ACCENT_CYAN, weight=BOLD).next_to(pop_title, DOWN, buff=0.25)
        pop_desc = Text("Citizens, ages, occupations,\nall recorded by hand.", font_size=16, color=TEXT_PRIMARY, line_spacing=1.3).next_to(pop_num, DOWN, buff=0.3)

        # Vector Tally Sheet Graphic
        tally_box = RoundedRectangle(corner_radius=0.1, width=4.5, height=1.3, fill_color="#0F172A", stroke_color="#334155")
        tally_box.next_to(pop_desc, DOWN, buff=0.35)
        tally_lines = VGroup(*[
            Line(ORIGIN, UP * 0.45, color="#64748B", stroke_width=2.5).shift(RIGHT * (i * 0.16 - 1.8))
            for i in range(20)
        ]).move_to(tally_box.get_center())
        # Add slash strokes
        slash1 = Line(LEFT * 0.4 + DOWN * 0.2, RIGHT * 0.4 + UP * 0.2, color=ACCENT_RED, stroke_width=2.5).move_to(tally_lines[2].get_center())
        slash2 = Line(LEFT * 0.4 + DOWN * 0.2, RIGHT * 0.4 + UP * 0.2, color=ACCENT_RED, stroke_width=2.5).move_to(tally_lines[12].get_center())
        tally_vector = VGroup(tally_box, tally_lines, slash1, slash2)

        card_left_content = VGroup(card_left, pop_title, pop_num, pop_desc, tally_vector)

        # Right Card: The 8-Year Arithmetic Delay
        card_right = create_card(5.6, 4.4)
        card_right.shift(RIGHT * 3.3 + DOWN * 0.4)

        time_title = Text("TALLY TIME REQUIREMENT", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(card_right.get_top() + DOWN * 0.45)
        years_num = Text("8 YEARS", font_size=38, color=ACCENT_RED, weight=BOLD).next_to(time_title, DOWN, buff=0.25)

        # Timeline Bar
        timeline_bg = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.28, fill_color="#1E293B", stroke_width=0)
        timeline_bg.next_to(years_num, DOWN, buff=0.4)
        timeline_fill = RoundedRectangle(corner_radius=0.1, width=3.7, height=0.28, fill_color=ACCENT_RED, stroke_width=0)
        timeline_fill.align_to(timeline_bg, LEFT)

        year_1880 = Text("1880", font_size=13, color=TEXT_MUTED).next_to(timeline_bg, DOWN, buff=0.15).align_to(timeline_bg, LEFT)
        year_1888 = Text("1888: Finished", font_size=13, color=ACCENT_RED, weight=BOLD).next_to(timeline_bg, DOWN, buff=0.15).shift(RIGHT * 0.8)
        year_1890 = Text("1890", font_size=13, color=TEXT_MUTED).next_to(timeline_bg, DOWN, buff=0.15).align_to(timeline_bg, RIGHT)

        crisis_alert = RoundedRectangle(corner_radius=0.12, width=4.8, height=1.0, fill_color="#3B1219", stroke_color=ACCENT_RED, stroke_width=1.5)
        crisis_alert.next_to(year_1888, DOWN, buff=0.35)
        crisis_txt = Text("CONSTITUTIONAL CRISIS\nNext census was due in 2 years.\nCount would outpace time itself.",
                          font_size=13, color="#FECACA", weight=BOLD, line_spacing=1.2).move_to(crisis_alert.get_center())

        card_right_content = VGroup(card_right, time_title, years_num, timeline_bg, timeline_fill, year_1880, year_1888, year_1890, crisis_alert, crisis_txt)

        self.play(FadeIn(card_left_content, shift=RIGHT * 0.4), run_time=1.2)
        self.play(FadeIn(card_right_content, shift=LEFT * 0.4), run_time=1.2)
        self.wait(3.0)

        # Core Lesson Callout for Census
        insight_banner = RoundedRectangle(corner_radius=0.15, width=10.0, height=0.85, fill_color="#0F172A", stroke_color=ACCENT_AMBER, stroke_width=1.8)
        insight_banner.to_edge(DOWN, buff=0.45)
        insight_txt = Text("Not a failure of human effort — but an absolute breakdown of scale.", font_size=17, color=TEXT_PRIMARY, weight=BOLD).move_to(insight_banner.get_center())
        insight_group = VGroup(insight_banner, insight_txt)

        self.play(FadeIn(insight_group, shift=UP * 0.3))
        self.wait(3.5)

        # Clean Act 1
        self.play(
            FadeOut(sec1_group),
            FadeOut(card_left_content),
            FadeOut(card_right_content),
            FadeOut(insight_group),
            run_time=0.9
        )

        # =========================================================
        # ACT 2: NAVIGATION & THE COST OF ARITHMETIC ERRORS
        # =========================================================
        sec2_badge = RoundedRectangle(corner_radius=0.1, width=4.8, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_CYAN, stroke_width=1.5)
        sec2_badge_lbl = Text("CASE 2: NAVIGATION & TABLES", font_size=15, color=ACCENT_CYAN, weight=BOLD)
        sec2_group = VGroup(sec2_badge, sec2_badge_lbl).to_edge(UP, buff=0.6)
        self.play(FadeIn(sec2_group, shift=DOWN * 0.2))

        # Vector Graphic: Ship & Nautical Compass on Left
        nav_card = create_card(5.6, 4.4).shift(LEFT * 3.3 + DOWN * 0.4)
        nav_card_title = Text("AT SEA: HUMAN COMPUTERS", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(nav_card.get_top() + DOWN * 0.45)

        # Clean Vector Sailing Vessel
        hull = Polygon([-1.8, -0.2, 0], [1.8, -0.2, 0], [1.3, -0.7, 0], [-1.4, -0.7, 0],
                       color=ACCENT_CYAN, fill_color="#1E3A5F", fill_opacity=0.8, stroke_width=2)
        mast1 = Line([ -0.4, -0.2, 0], [ -0.4, 1.2, 0], color=TEXT_PRIMARY, stroke_width=2.5)
        mast2 = Line([ 0.5, -0.2, 0], [ 0.5, 0.9, 0], color=TEXT_PRIMARY, stroke_width=2.5)
        sail1 = Polygon([-0.4, 0.0, 0], [0.3, 0.5, 0], [-0.4, 1.0, 0], color=TEXT_PRIMARY, fill_color=TEXT_PRIMARY, fill_opacity=0.8)
        sail2 = Polygon([0.5, 0.0, 0], [1.1, 0.4, 0], [0.5, 0.8, 0], color=TEXT_PRIMARY, fill_color=TEXT_PRIMARY, fill_opacity=0.7)
        waves = VGroup(*[
            Arc(radius=0.4, start_angle=PI, angle=-PI, stroke_color="#38BDF8", stroke_width=2).shift(RIGHT * (i * 0.7 - 1.4) + DOWN * 0.8)
            for i in range(5)
        ])
        ship_vector = VGroup(hull, mast1, mast2, sail1, sail2, waves).scale(0.85).next_to(nav_card_title, DOWN, buff=0.4)

        nav_note = Text("Job Title: 'Computer'\nHumans computing logarithms\nand astronomical positions.",
                        font_size=14, color=TEXT_PRIMARY, line_spacing=1.3).next_to(ship_vector, DOWN, buff=0.35)
        nav_card_group = VGroup(nav_card, nav_card_title, ship_vector, nav_note)

        # Right Card: The Printed Table Error Ripple
        table_card = create_card(5.6, 4.4).shift(RIGHT * 3.3 + DOWN * 0.4)
        table_card_title = Text("MATHEMATICAL TABLES", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(table_card.get_top() + DOWN * 0.45)

        # Vector Table Grid
        table_grid = VGroup()
        rows, cols = 4, 3
        cell_w, cell_h = 1.3, 0.42
        for r in range(rows):
            for c in range(cols):
                box = Rectangle(width=cell_w, height=cell_h, stroke_color="#334155", stroke_width=1.2, fill_color="#0F172A", fill_opacity=0.6)
                box.move_to(np.array([(c - 1) * cell_w, (1.5 - r) * cell_h, 0]))
                val_str = f"{(r+1)*12.4 + c*3.14:.2f}"
                val_txt = Text(val_str, font_size=12, color=TEXT_PRIMARY)
                val_txt.move_to(box.get_center())
                table_grid.add(VGroup(box, val_txt))
        table_grid.next_to(table_card_title, DOWN, buff=0.3)

        # Highlighting a Human Typo/Math Error
        err_box = Rectangle(width=cell_w, height=cell_h, stroke_color=ACCENT_RED, stroke_width=2.5, fill_color="#7F1D1D", fill_opacity=0.9)
        err_box.move_to(table_grid[5][0].get_center())
        err_txt = Text("ERR!", font_size=13, color="#FFFFFF", weight=BOLD).move_to(err_box.get_center())
        error_cell = VGroup(err_box, err_txt)

        vasa_card = RoundedRectangle(corner_radius=0.1, width=4.8, height=1.05, fill_color="#2E1015", stroke_color=ACCENT_RED, stroke_width=1.5)
        vasa_card.next_to(table_grid, DOWN, buff=0.35)
        vasa_text = Text("CATASTROPHIC CONSEQUENCE:\nSwedish warship 'Vasa' (1628) sank due to\ncalculation flaws. Navigators ran ships on rocks.",
                         font_size=12, color="#FECACA", weight=BOLD, line_spacing=1.2).move_to(vasa_card.get_center())
        table_card_group = VGroup(table_card, table_card_title, table_grid, vasa_card, vasa_text)

        self.play(FadeIn(nav_card_group, shift=RIGHT * 0.3), FadeIn(table_card_group, shift=LEFT * 0.3), run_time=1.2)
        self.wait(1.5)
        self.play(Transform(table_grid[5], error_cell), run_time=0.8)
        self.wait(3.5)

        # Clean Act 2
        self.play(FadeOut(sec2_group), FadeOut(nav_card_group), FadeOut(table_card_group), run_time=0.9)

        # =========================================================
        # ACT 3: ARTILLERY & WARTIME CALCULATION (ENIAC)
        # =========================================================
        sec3_badge = RoundedRectangle(corner_radius=0.1, width=5.2, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_PURPLE, stroke_width=1.5)
        sec3_badge_lbl = Text("CASE 3: BALLISTICS & WARTIME", font_size=15, color=ACCENT_PURPLE, weight=BOLD)
        sec3_group = VGroup(sec3_badge, sec3_badge_lbl).to_edge(UP, buff=0.6)
        self.play(FadeIn(sec3_group, shift=DOWN * 0.2))

        # Left Card: Vector Trajectory Simulation
        traj_card = create_card(5.6, 4.4).shift(LEFT * 3.3 + DOWN * 0.4)
        traj_title = Text("ARTILLERY FIRING TABLES", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(traj_card.get_top() + DOWN * 0.45)

        # Parabolic Trajectory
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 5, 2], x_length=4.2, y_length=2.0, tips=False,
                    axis_config={"color": "#475569", "stroke_width": 1.5})
        trajectory_curve = axes.plot(lambda x: -0.16 * (x - 5)**2 + 4, x_range=[0, 10], color=ACCENT_AMBER, stroke_width=3)
        cannon_pt = Dot(axes.c2p(0, 0), color=ACCENT_CYAN, radius=0.08)
        target_pt = Dot(axes.c2p(10, 0), color=ACCENT_RED, radius=0.08)
        target_ring = Circle(radius=0.22, color=ACCENT_RED, stroke_width=1.5).move_to(axes.c2p(10, 0))

        traj_plot = VGroup(axes, trajectory_curve, cannon_pt, target_pt, target_ring).next_to(traj_title, DOWN, buff=0.3)
        traj_desc = Text("Thousands of calculations per gun:\nwind, humidity, elevation, projectile mass.",
                         font_size=13, color=TEXT_PRIMARY, line_spacing=1.2).next_to(traj_plot, DOWN, buff=0.3)
        traj_group = VGroup(traj_card, traj_title, traj_plot, traj_desc)

        # Right Card: The Aberdeen Human Bottleneck & ENIAC
        eniac_card = create_card(5.6, 4.4).shift(RIGHT * 3.3 + DOWN * 0.4)
        eniac_title = Text("HUMAN SPEED BOTTLENECK", font_size=17, color=TEXT_MUTED, weight=BOLD).move_to(eniac_card.get_top() + DOWN * 0.45)

        stat_human = VGroup(
            Text("HUMAN COMPUTER (1942)", font_size=13, color=TEXT_MUTED, weight=BOLD),
            Text("Days to compute 1 trajectory", font_size=18, color=ACCENT_RED, weight=BOLD)
        ).arrange(DOWN, buff=0.15).next_to(eniac_title, DOWN, buff=0.4)

        down_arrow = Arrow(UP * 0.5, DOWN * 0.5, color=ACCENT_CYAN, stroke_width=3).next_to(stat_human, DOWN, buff=0.25)

        stat_eniac = VGroup(
            Text("ENIAC ELECTRONIC (1945)", font_size=13, color=ACCENT_GREEN, weight=BOLD),
            Text("20 Seconds per trajectory", font_size=20, color=ACCENT_GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.15).next_to(down_arrow, DOWN, buff=0.25)

        fund_note = Text("Speed became a strategic survival priority.", font_size=13, color=TEXT_MUTED).next_to(stat_eniac, DOWN, buff=0.35)
        eniac_group = VGroup(eniac_card, eniac_title, stat_human, down_arrow, stat_eniac, fund_note)

        self.play(FadeIn(traj_group, shift=RIGHT * 0.3), FadeIn(eniac_group, shift=LEFT * 0.3), run_time=1.2)
        self.play(Create(trajectory_curve), run_time=1.4)
        self.wait(3.5)

        # Clean Act 3
        self.play(FadeOut(sec3_group), FadeOut(traj_group), FadeOut(eniac_group), run_time=0.9)

        # =========================================================
        # ACT 4: THE UNIVERSAL PATTERN
        # =========================================================
        sec4_badge = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_CYAN, stroke_width=1.5)
        sec4_badge_lbl = Text("THE RECURRING PATTERN", font_size=15, color=ACCENT_CYAN, weight=BOLD)
        sec4_group = VGroup(sec4_badge, sec4_badge_lbl).to_edge(UP, buff=0.6)
        self.play(FadeIn(sec4_group, shift=DOWN * 0.2))

        # Comparison Grid
        matrix_bg = create_card(11.2, 4.0).shift(DOWN * 0.3)

        # Header Row
        h1 = Text("PROBLEM", font_size=15, color=ACCENT_CYAN, weight=BOLD).move_to(matrix_bg.get_top() + DOWN * 0.45 + LEFT * 3.6)
        h2 = Text("SCALE", font_size=15, color=ACCENT_AMBER, weight=BOLD).move_to(matrix_bg.get_top() + DOWN * 0.45)
        h3 = Text("CONSEQUENCE OF SLOWNESS", font_size=15, color=ACCENT_RED, weight=BOLD).move_to(matrix_bg.get_top() + DOWN * 0.45 + RIGHT * 3.3)
        h_line = Line(LEFT * 5.2, RIGHT * 5.2, color="#334155", stroke_width=1.5).next_to(h1, DOWN, buff=0.2).align_to(matrix_bg, LEFT).shift(RIGHT * 0.4)

        # Row 1
        r1_a = Text("Census Tallying", font_size=14, color=TEXT_PRIMARY).move_to(h1.get_center() + DOWN * 0.7)
        r1_b = Text("50 Million Records", font_size=14, color=TEXT_MUTED).move_to(h2.get_center() + DOWN * 0.7)
        r1_c = Text("Governmental Paralysis", font_size=14, color=TEXT_PRIMARY).move_to(h3.get_center() + DOWN * 0.7)

        # Row 2
        r2_a = Text("Navigational Tables", font_size=14, color=TEXT_PRIMARY).move_to(r1_a.get_center() + DOWN * 0.65)
        r2_b = Text("Millions of Ops", font_size=14, color=TEXT_MUTED).move_to(r1_b.get_center() + DOWN * 0.65)
        r2_c = Text("Shipwrecks & Lost Lives", font_size=14, color=TEXT_PRIMARY).move_to(r1_c.get_center() + DOWN * 0.65)

        # Row 3
        r3_a = Text("Ballistics / Trajectories", font_size=14, color=TEXT_PRIMARY).move_to(r2_a.get_center() + DOWN * 0.65)
        r3_b = Text("Thousands of Ballistic Runs", font_size=14, color=TEXT_MUTED).move_to(r2_b.get_center() + DOWN * 0.65)
        r3_c = Text("Strategic Military Liability", font_size=14, color=TEXT_PRIMARY).move_to(r2_c.get_center() + DOWN * 0.65)

        matrix_content = VGroup(matrix_bg, h1, h2, h3, h_line, r1_a, r1_b, r1_c, r2_a, r2_b, r2_c, r3_a, r3_b, r3_c)

        self.play(FadeIn(matrix_content, shift=UP * 0.3), run_time=1.3)
        self.wait(3.0)

        # Single Bottleneck Takeaway Banner
        takeaway_card = RoundedRectangle(corner_radius=0.15, width=11.2, height=0.9, fill_color="#1E293B", stroke_color=ACCENT_CYAN, stroke_width=2)
        takeaway_card.to_edge(DOWN, buff=0.45)
        takeaway_txt = Text("THE BOTTLENECK: Humans doing repetitive arithmetic at scale.",
                            font_size=18, color=ACCENT_CYAN, weight=BOLD).move_to(takeaway_card.get_center())
        takeaway_group = VGroup(takeaway_card, takeaway_txt)

        self.play(FadeIn(takeaway_group, shift=UP * 0.3))
        self.wait(3.5)

        self.play(FadeOut(sec4_group), FadeOut(matrix_content), FadeOut(takeaway_group), run_time=0.9)

        # =========================================================
        # ACT 5: WHAT IS COMPUTATION? (SYMBOL, RULE, MANIPULATION)
        # =========================================================
        sec5_badge = RoundedRectangle(corner_radius=0.1, width=5.6, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_GREEN, stroke_width=1.5)
        sec5_badge_lbl = Text("THE CONCEPT: WHAT IS COMPUTATION?", font_size=15, color=ACCENT_GREEN, weight=BOLD)
        sec5_group = VGroup(sec5_badge, sec5_badge_lbl).to_edge(UP, buff=0.6)
        self.play(FadeIn(sec5_group, shift=DOWN * 0.2))

        # 3 Pillar Pillars: Symbol -> Rule -> Manipulation
        pillar_w, pillar_h = 3.4, 3.2

        p1_card = create_card(pillar_w, pillar_h).shift(LEFT * 3.8 + DOWN * 0.1)
        p1_title = Text("1. SYMBOL", font_size=18, color=ACCENT_CYAN, weight=BOLD).move_to(p1_card.get_top() + DOWN * 0.4)
        p1_desc = Text("Any information\nrepresentation:\n- Number\n- Character\n- Hole in a punch card",
                       font_size=13, color=TEXT_PRIMARY, line_spacing=1.3).next_to(p1_title, DOWN, buff=0.3)
        p1 = VGroup(p1_card, p1_title, p1_desc)

        arrow1 = Arrow(LEFT * 0.5, RIGHT * 0.5, color=TEXT_MUTED, stroke_width=3).move_to(LEFT * 1.9 + DOWN * 0.1)

        p2_card = create_card(pillar_w, pillar_h).shift(DOWN * 0.1)
        p2_title = Text("2. RULE", font_size=18, color=ACCENT_AMBER, weight=BOLD).move_to(p2_card.get_top() + DOWN * 0.4)
        p2_desc = Text("A defined, unambiguous\noperation:\n- Add these two\n- Shift bits left\n- Check condition",
                       font_size=13, color=TEXT_PRIMARY, line_spacing=1.3).next_to(p2_title, DOWN, buff=0.3)
        p2 = VGroup(p2_card, p2_title, p2_desc)

        arrow2 = Arrow(LEFT * 0.5, RIGHT * 0.5, color=TEXT_MUTED, stroke_width=3).move_to(RIGHT * 1.9 + DOWN * 0.1)

        p3_card = create_card(pillar_w, pillar_h).shift(RIGHT * 3.8 + DOWN * 0.1)
        p3_title = Text("3. MANIPULATION", font_size=18, color=ACCENT_PURPLE, weight=BOLD).move_to(p3_card.get_top() + DOWN * 0.4)
        p3_desc = Text("Applying the rule\nto produce a new\noutput symbol:\n- Long division\n- Gear rotation\n- Transistor switch",
                       font_size=13, color=TEXT_PRIMARY, line_spacing=1.3).next_to(p3_title, DOWN, buff=0.3)
        p3 = VGroup(p3_card, p3_title, p3_desc)

        computation_flow = VGroup(p1, arrow1, p2, arrow2, p3)
        self.play(LaggedStart(FadeIn(p1, shift=UP * 0.2), GrowArrow(arrow1), FadeIn(p2, shift=UP * 0.2), GrowArrow(arrow2), FadeIn(p3, shift=UP * 0.2), lag_ratio=0.25), run_time=2.0)
        self.wait(3.5)

        # Machine Advantage Matrix Bottom
        adv_card = create_card(11.2, 1.3).to_edge(DOWN, buff=0.45)
        adv_c1 = VGroup(Text("SPEED", font_size=13, color=ACCENT_CYAN, weight=BOLD), Text("Milliseconds -> Nanoseconds", font_size=12, color=TEXT_PRIMARY)).arrange(DOWN, buff=0.1).move_to(adv_card.get_center() + LEFT * 3.6)
        adv_c2 = VGroup(Text("RELIABILITY", font_size=13, color=ACCENT_GREEN, weight=BOLD), Text("Circuits don't drift or forget", font_size=12, color=TEXT_PRIMARY)).arrange(DOWN, buff=0.1).move_to(adv_card.get_center())
        adv_c3 = VGroup(Text("TIRELESSNESS", font_size=13, color=ACCENT_AMBER, weight=BOLD), Text("Machines run 10^9 cycles", font_size=12, color=TEXT_PRIMARY)).arrange(DOWN, buff=0.1).move_to(adv_card.get_center() + RIGHT * 3.6)
        adv_group = VGroup(adv_card, adv_c1, adv_c2, adv_c3)

        self.play(FadeIn(adv_group, shift=UP * 0.3))
        self.wait(3.5)

        self.play(FadeOut(sec5_group), FadeOut(computation_flow), FadeOut(adv_group), run_time=0.9)

        # =========================================================
        # ACT 6: PREVIEW OF STORED INSTRUCTIONS & OUTRO
        # =========================================================
        next_tag = RoundedRectangle(corner_radius=0.1, width=3.2, height=0.5, fill_color=CARD_BG, stroke_color=ACCENT_CYAN, stroke_width=1.5).to_edge(UP, buff=1.0)
        next_tag_lbl = Text("WHAT COMES NEXT", font_size=15, color=ACCENT_CYAN, weight=BOLD).move_to(next_tag.get_center())

        big_idea = Text("The Leap: Stored Instructions", font_size=36, weight=BOLD, color=TEXT_PRIMARY).next_to(next_tag, DOWN, buff=0.4)
        big_idea_sub = Text("A machine that not only calculates, but reads and executes its own program.",
                            font_size=18, color=TEXT_MUTED).next_to(big_idea, DOWN, buff=0.25)

        # Vector Stepper preview
        step_box1 = RoundedRectangle(corner_radius=0.1, width=2.6, height=1.1, fill_color=CARD_BG, stroke_color="#334155")
        step_txt1 = Text("Module 0.3\nJacquard Loom", font_size=13, color=TEXT_PRIMARY, line_spacing=1.2).move_to(step_box1.get_center())
        s1 = VGroup(step_box1, step_txt1).shift(LEFT * 3.6 + DOWN * 1.1)

        step_box2 = RoundedRectangle(corner_radius=0.1, width=2.6, height=1.1, fill_color=CARD_BG, stroke_color="#334155")
        step_txt2 = Text("Module 0.4\nBabbage Engine", font_size=13, color=TEXT_PRIMARY, line_spacing=1.2).move_to(step_box2.get_center())
        s2 = VGroup(step_box2, step_txt2).shift(DOWN * 1.1)

        step_box3 = RoundedRectangle(corner_radius=0.1, width=2.6, height=1.1, fill_color=CARD_BG, stroke_color=ACCENT_CYAN, stroke_width=2)
        step_txt3 = Text("Module 0.5\nHollerith Census", font_size=13, color=ACCENT_CYAN, weight=BOLD, line_spacing=1.2).move_to(step_box3.get_center())
        s3 = VGroup(step_box3, step_txt3).shift(RIGHT * 3.6 + DOWN * 1.1)

        a_next1 = Arrow(s1.get_right(), s2.get_left(), color=TEXT_MUTED, stroke_width=2.5)
        a_next2 = Arrow(s2.get_right(), s3.get_left(), color=TEXT_MUTED, stroke_width=2.5)

        lab_callout = RoundedRectangle(corner_radius=0.12, width=9.2, height=0.75, fill_color="#0F172A", stroke_color=ACCENT_AMBER, stroke_width=1.5)
        lab_callout.to_edge(DOWN, buff=0.8)
        lab_callout_txt = Text("TRY IT NOW: Launch simulation.html to test your human tally limit",
                               font_size=14, color=ACCENT_AMBER, weight=BOLD).move_to(lab_callout.get_center())
        callout_group = VGroup(lab_callout, lab_callout_txt)

        self.play(FadeIn(next_tag), FadeIn(next_tag_lbl), Write(big_idea), FadeIn(big_idea_sub, shift=UP * 0.2))
        self.play(LaggedStart(FadeIn(s1), GrowArrow(a_next1), FadeIn(s2), GrowArrow(a_next2), FadeIn(s3), lag_ratio=0.2), run_time=1.6)
        self.play(FadeIn(callout_group, shift=UP * 0.3))
        self.wait(4.0)

        # Outro Fade
        self.play(
            FadeOut(title),
            FadeOut(next_tag),
            FadeOut(next_tag_lbl),
            FadeOut(big_idea),
            FadeOut(big_idea_sub),
            FadeOut(s1),
            FadeOut(s2),
            FadeOut(s3),
            FadeOut(a_next1),
            FadeOut(a_next2),
            FadeOut(callout_group),
            run_time=1.5
        )
        self.wait(1.0)


if __name__ == "__main__":
    from manim.__main__ import main
    if len(sys.argv) == 1:
        sys.argv = ["manim", "-ql", os.path.abspath(__file__), "WhyComputeScene"]
    else:
        file_path = os.path.abspath(__file__)
        user_args = sys.argv[1:]
        # Append file and scene name if not already provided
        if file_path not in user_args and "WhyComputeScene" not in user_args:
            sys.argv = ["manim"] + user_args + [file_path, "WhyComputeScene"]
        else:
            sys.argv = ["manim"] + user_args
    main()
