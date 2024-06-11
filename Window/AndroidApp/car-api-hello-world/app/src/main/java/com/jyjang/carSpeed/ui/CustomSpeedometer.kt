package com.jyjang.carSpeed.ui

import android.content.Context
import android.util.AttributeSet
import com.github.anastr.speedviewlib.AwesomeSpeedometer

class CustomSpeedometer @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0,
) : AwesomeSpeedometer(context, attrs, defStyleAttr) {

    init {
        // 초기화 시 텍스트 크기를 설정합니다.
        textPaint.textSize = 40f // 원하는 텍스트 크기로 설정
    }

    // 텍스트 크기를 동적으로 변경하는 메서드
    fun setCustomTextSize(size: Float) {
        textPaint.textSize = size
        invalidateGauge()
    }
}