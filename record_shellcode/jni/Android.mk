LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_CFLAGS += -pie -fPIE
LOCAL_LDFLAGS += -pie -fPIE
LOCAL_MODULE    := record_asm
LOCAL_SRC_FILES := record.s
LOCAL_ARM_MODE := arm

include $(BUILD_EXECUTABLE)
