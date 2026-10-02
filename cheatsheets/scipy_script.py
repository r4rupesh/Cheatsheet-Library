from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import streamlit as st
from code_editor import code_editor
from pynteract import Shell
from scipy import integrate, optimize, signal, stats

from .paths import REFERENCE_DIR


def run_scipy_code(source_code):
    plt.close("all")
    shell = st.session_state.get("scipy_code_shell")
    if shell is None:
        shell = Shell(
            namespace={
                "np": np,
                "sp": sp,
                "integrate": integrate,
                "optimize": optimize,
                "stats": stats,
                "signal": signal,
                "plt": plt,
            },
            silent=True,
            display_mode="last",
        )
        st.session_state["scipy_code_shell"] = shell

    response = shell.run(source_code, filename="scipy_playground.py")
    images = []
    for figure_number in plt.get_fignums():
        figure = plt.figure(figure_number)
        image_buffer = BytesIO()
        figure.savefig(image_buffer, format="png", dpi=180, bbox_inches="tight")
        images.append(image_buffer.getvalue())
        plt.close(figure)
    error = str(response.exception) if response.exception else response.stderr
    return response.stdout, error, images


def scipy_cheatsheet():
    st.set_page_config(page_title="CheatSheets | SciPy", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "scipy_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    st.title("SciPy cheatsheet")
    reference_tab, playground_tab = st.tabs(["Cheatsheet", "Playground"])

    with reference_tab:
        st.download_button(
            "Download reference",
            data=reference_file.read_bytes(),
            file_name=reference_file.name,
            mime="text/markdown",
            icon=":material/download:",
        )
        st.markdown(reference_file.read_text(encoding="utf-8"))

    with playground_tab:
        operation = st.selectbox(
            "SciPy tool",
            ["Integration", "Optimization", "Statistics", "Signal filtering"],
            key="scipy_operation",
        )
        if operation == "Integration":
            upper_bound = st.slider("Upper bound", 0.5, 12.0, 3.14, 0.1, key="scipy_integral_upper")
            result, error_estimate = integrate.quad(np.sin, 0, upper_bound)
            st.metric("Integral of sin(x) from 0 to upper bound", f"{result:.8f}")
            st.caption(f"Estimated absolute error: {error_estimate:.2e}")
        elif operation == "Optimization":
            target = st.slider("Target location", -8.0, 8.0, 2.5, 0.1, key="scipy_opt_target")
            result = optimize.minimize_scalar(
                lambda value: (value - target) ** 2 + 3,
                bounds=(-10, 10),
                method="bounded",
            )
            st.metric("Minimum x", f"{result.x:.6f}")
            st.caption(f"Minimum function value: {result.fun:.6f} · success: {result.success}")
        elif operation == "Statistics":
            controls = st.columns(3)
            location = controls[0].slider("Mean (loc)", -10.0, 10.0, 0.0, 0.5, key="scipy_stats_loc")
            scale = controls[1].slider("Standard deviation (scale)", 0.2, 5.0, 1.5, 0.1, key="scipy_stats_scale")
            value = controls[2].slider("Evaluate at x", -10.0, 10.0, 1.0, 0.5, key="scipy_stats_x")
            distribution = stats.norm(loc=location, scale=scale)
            metrics = st.columns(3)
            metrics[0].metric("PDF", f"{distribution.pdf(value):.5f}")
            metrics[1].metric("CDF", f"{distribution.cdf(value):.5f}")
            metrics[2].metric("90th percentile", f"{distribution.ppf(0.9):.4f}")
        else:
            controls = st.columns(3)
            frequency = controls[0].slider("Signal frequency", 1, 12, 3, key="scipy_signal_frequency")
            noise_level = controls[1].slider("Noise level", 0.0, 1.0, 0.35, 0.05, key="scipy_signal_noise")
            window_length = controls[2].selectbox("Smoothing window", [5, 9, 15, 21], index=2, key="scipy_signal_window")
            time = np.linspace(0, 1, 250)
            rng = np.random.default_rng(42)
            clean_signal = np.sin(2 * np.pi * frequency * time)
            noisy_signal = clean_signal + rng.normal(0, noise_level, size=time.size)
            filtered_signal = signal.savgol_filter(noisy_signal, window_length=window_length, polyorder=2)
            figure, axes = plt.subplots(figsize=(10, 4), layout="constrained")
            axes.plot(time, noisy_signal, color="#8A9AA8", alpha=0.45, label="Noisy")
            axes.plot(time, filtered_signal, color="#167D63", linewidth=2.3, label="Smoothed")
            axes.set(xlabel="Time (s)", ylabel="Amplitude", title="Savitzky-Golay smoothing")
            axes.legend(frameon=False)
            axes.spines[["top", "right"]].set_visible(False)
            axes.grid(axis="y", alpha=0.2)
            st.pyplot(figure, width="stretch")
            plt.close(figure)

        st.subheader("Write your own SciPy code")
        st.caption("Code runs on this app's server. Run only code you trust. NumPy, SciPy modules, and `plt` are ready to use.")
        starter_code = '''x = np.linspace(0, np.pi, 100)
area, estimated_error = integrate.quad(np.sin, 0, np.pi)

print(f"Integral: {area:.6f}")
print(f"Estimated error: {estimated_error:.2e}")
'''
        st.session_state.setdefault("scipy_user_code", starter_code)
        editor_response = code_editor(
            st.session_state["scipy_user_code"],
            lang="python",
            height=270,
            response_mode=["debounce", "blur"],
            key="scipy_user_code_editor",
        )
        if editor_response.get("type"):
            st.session_state["scipy_user_code"] = editor_response.get("text", "")

        if st.button("Run SciPy code", icon=":material/play_arrow:", key="run_scipy_user_code"):
            output, error, images = run_scipy_code(st.session_state["scipy_user_code"])
            st.session_state["scipy_user_output"] = output
            st.session_state["scipy_user_error"] = error
            st.session_state["scipy_user_images"] = images

        if st.session_state.get("scipy_user_output"):
            st.code(st.session_state["scipy_user_output"], language="text")
        if st.session_state.get("scipy_user_error"):
            st.error(st.session_state["scipy_user_error"])
        for image in st.session_state.get("scipy_user_images", []):
            st.image(image)
