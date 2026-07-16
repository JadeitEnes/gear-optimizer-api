from enum import Enum


class UsagePurpose(str, Enum):
    GAMING_GPU_INTENSIVE = "gaming_gpu_intensive"
    GAMING_CPU_INTENSIVE = "gaming_cpu_intensive"
    GAMING_BALANCED = "gaming_balanced"
    VIDEO_EDITING = "video_editing"
    SOFTWARE_DEVELOPMENT = "software_development"