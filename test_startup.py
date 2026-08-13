"""Side-effect-free checks for startup status and recovery messages."""

from unittest.mock import patch

from kloom import startup_failure_message
from stt import Stt, configured_status


def test_configured_status_uses_model_and_device_from_config():
    assert configured_status({"stt": {"model": "small", "device": "cpu"}}) == (
        "Whisper small en CPU"
    )
    assert configured_status({"stt": {"model": "large-v3", "device": "cuda"}}) == (
        "Whisper large-v3 en GPU"
    )


def test_microphone_failure_messages_are_actionable():
    assert "audio.capture_sample_rate" in startup_failure_message(
        "micrófono", RuntimeError("Invalid sample rate")
    )
    assert "dispositivo válido" in startup_failure_message(
        "micrófono", RuntimeError("PortAudio error")
    )


def test_stt_status_reports_cpu_after_cuda_fallback():
    with patch("stt.WhisperModel", side_effect=[RuntimeError("no CUDA"), object()]):
        stt = Stt({"stt": {"model": "large-v3", "device": "cuda"}})

    assert stt.status == "Whisper medium en CPU"


def test_stt_failure_message_points_to_configuration():
    message = startup_failure_message("reconocimiento de voz", RuntimeError("CUDA failed"))

    assert "modelo" in message
    assert "config.yaml" in message


if __name__ == "__main__":
    test_configured_status_uses_model_and_device_from_config()
    test_microphone_failure_messages_are_actionable()
    test_stt_status_reports_cpu_after_cuda_fallback()
    test_stt_failure_message_points_to_configuration()
    print("startup checks OK")
