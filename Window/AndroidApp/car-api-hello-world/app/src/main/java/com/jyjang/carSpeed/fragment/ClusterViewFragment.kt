package com.jyjang.carSpeed

import android.Manifest
import android.animation.ValueAnimator
import android.car.Car
import android.car.VehiclePropertyIds
import android.car.hardware.CarPropertyValue
import android.car.hardware.property.CarPropertyManager
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.PorterDuff
import android.graphics.PorterDuffColorFilter
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import com.example.carapihelloworld.R
import com.github.anastr.speedviewlib.AwesomeSpeedometer
import com.jyjang.carSpeed.model.CarPropertyManagerSingleton

class ClusterViewFragment : Fragment() {
    private val BLUE = Color.parseColor("#00BFFF") // 초록
    private val GREEN = Color.parseColor("#66BB6A") // 초록
    private val YELLOW = Color.parseColor("#FFFF00")
    private val WHITE = Color.parseColor("#FFFFFF")
    private val RED = Color.parseColor("#D1180B")  // 빨간색

    private lateinit var mCarPropertyManager: CarPropertyManager

    private lateinit var chargePortConnectImage: ImageView
    private lateinit var chargePortOpenImage: ImageView
    private lateinit var autoParkingImage: ImageView
    private lateinit var batteryImage: ImageView

    private lateinit var parkGearImage: TextView
    private lateinit var reverseGearImage: TextView
    private lateinit var driveGearImage: TextView
    private lateinit var neutralGearImage: TextView

    private lateinit var ignitionTextView: TextView

    private lateinit var evBatteryTextView: TextView
    private lateinit var evChargeTimeRemaining: TextView

    companion object {
        private const val TAG = "ClusterViewFragment"
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_cluster_view, container, false)

        chargePortOpenImage = view.findViewById(R.id.charge_port_open_image)
        chargePortConnectImage = view.findViewById(R.id.charge_port_connect_image)
        autoParkingImage = view.findViewById(R.id.auto_parking_image)
        batteryImage = view.findViewById(R.id.battery)

        parkGearImage = view.findViewById(R.id.park_gear_text)
        reverseGearImage = view.findViewById(R.id.reverse_gear_text)
        driveGearImage = view.findViewById(R.id.drive_gear_text)
        neutralGearImage = view.findViewById(R.id.neutral_gear_text)

        ignitionTextView = view.findViewById(R.id.ignition_state_text)

        evBatteryTextView = view.findViewById(R.id.ev_battery_textview)
        evChargeTimeRemaining = view.findViewById(R.id.ev_charge_time_remaining)

        return view
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        initCarPropertyManager()
        registerCallback()
    }
    private fun initCarPropertyManager() {
        mCarPropertyManager =  CarPropertyManagerSingleton.getInstance(requireContext()).carPropertyManager
    }

    private fun registerCallback() {
        // EV_CHARGE_PORT_OPEN
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Boolean
                Log.d(TAG, "$propertyId (EV_CHARGE_PORT_OPEN) Set $propertyValue")
                setImageViewPropValue(chargePortOpenImage, propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.EV_CHARGE_PORT_OPEN, CarPropertyManager.SENSOR_RATE_NORMAL)

        // EV_CHARGE_PORT_CONNECTED
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Boolean
                Log.d(TAG, "$propertyId (EV_CHARGE_PORT_CONNECTED) Set $propertyValue")
                setImageViewPropValue(chargePortConnectImage, propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.EV_CHARGE_PORT_CONNECTED, CarPropertyManager.SENSOR_RATE_NORMAL)

        // PARKING_BRAKE_AUTO_APPLY
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Boolean
                Log.d(TAG, "$propertyId (PARKING_BRAKE_AUTO_APPLY)is Change $propertyValue")
                setImageViewPropValue(autoParkingImage, propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.PARKING_BRAKE_AUTO_APPLY, CarPropertyManager.SENSOR_RATE_NORMAL)


        // GEAR_SELECTION
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Int
                Log.d(TAG, "$propertyId (GEAR_SELECTION) Set $propertyValue")
                setGearSelectionValue(propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.GEAR_SELECTION, CarPropertyManager.SENSOR_RATE_NORMAL)



        // PERCEIVED_SPEED
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Float
                Log.d(TAG, "$propertyId (PERF_VEHICLE_SPEED)is Change $propertyValue")
                view?.findViewById<AwesomeSpeedometer>(R.id.awesomeSpeedometer)
                    ?.speedTo(propertyValue)

                val speedometerValue =  view?.findViewById<TextView>(R.id.speedometerValue)
                if (speedometerValue != null) {
                    animateSpeedometerValue(speedometerValue, propertyValue)
                }
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.PERF_VEHICLE_SPEED_DISPLAY, CarPropertyManager.SENSOR_RATE_NORMAL)

        // IGNITION_STATE
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Int
                Log.d(TAG, "$propertyId (IGNITION_STATE) Set $propertyValue")
                setIgnitionState(ignitionTextView, propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.IGNITION_STATE, CarPropertyManager.SENSOR_RATE_NORMAL)

        // EV_BATTERY_LEVEL
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val evCurrentBattery = mCarPropertyManager.getFloatProperty(VehiclePropertyIds.INFO_EV_BATTERY_CAPACITY, 0)
                Log.d(TAG, "(EV_CURRENT_BATTERY_CAPACITY) is value $evCurrentBattery")
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Float
                Log.d(TAG, "$propertyId (EV_BATTERY_LEVEL) is Change $propertyValue")
                val batteryTotal = (propertyValue / evCurrentBattery) * 100
                val batteryPercentage = batteryTotal.toInt()
                evBatteryTextView.text = batteryPercentage.toString()

                // 배터리 수준에 따라 텍스트 및 이미지 색상 변경
                if (isCharging() == 1) {
                    batteryImage.colorFilter = PorterDuffColorFilter(GREEN, PorterDuff.Mode.SRC_ATOP)
                } else if (batteryPercentage < 20) {
                    batteryImage.colorFilter = PorterDuffColorFilter(RED, PorterDuff.Mode.SRC_ATOP)
                } else {
                    batteryImage.colorFilter = null
                }
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.EV_BATTERY_LEVEL, CarPropertyManager.SENSOR_RATE_NORMAL)
    }
    // 애니메이션 메서드
    private fun animateSpeedometerValue(speedometerValue: TextView, newValue: Float) {
        val currentSpeedText = speedometerValue.text.toString()
        val currentSpeed: Float = try {
            currentSpeedText.toFloat()
        } catch (e: NumberFormatException) {
            0f
        }

        val animator = ValueAnimator.ofFloat(currentSpeed, newValue)
        animator.duration = 500 // 애니메이션 지속 시간 (밀리초)
        animator.addUpdateListener { animation ->
            val animatedValue = animation.animatedValue as Float
            speedometerValue.text = String.format("%.0f", animatedValue)
        }
        animator.start()
    }

    private fun setGearSelectionValue(value: Int) {
        when (value) {
            0 -> setGear(parkGearImage)
            1 -> setGear(reverseGearImage)
            2 -> setGear(neutralGearImage)
            3 -> setGear(driveGearImage)
        }
    }

    private fun setGear(gearTextView: TextView) {
        val gears = listOf(parkGearImage, reverseGearImage, neutralGearImage, driveGearImage)
        for (gear in gears) {
            gear.setTextColor(WHITE)
        }
        gearTextView.setTextColor(YELLOW)
    }

    private fun setImageViewPropValue(imageView: ImageView, value: Boolean) {
        if (value) {
            imageView.colorFilter = PorterDuffColorFilter(BLUE, PorterDuff.Mode.SRC_IN)
        } else {
            imageView.colorFilter = PorterDuffColorFilter(WHITE, PorterDuff.Mode.SRC_IN)
        }
    }

    // 충전 상태를 확인하는 함수
    private fun isCharging(): Int {
        return try {
            val isCharging = mCarPropertyManager.getIntProperty(VehiclePropertyIds.EV_CHARGE_STATE, 0)
            Log.d(TAG, "EV_CHARGE_STATE value: $isCharging")

            when(isCharging) {
                1 -> Log.d(TAG, "Charging status: Charging")
                2 -> Log.d(TAG, "Charging status: Fully charged")
                3 -> Log.d(TAG, "Charging status: Not charging")
                else -> Log.d(TAG, "Charging status: Unknown value $isCharging")
            }

            isCharging
        } catch (e: Exception) {
            Log.e(TAG, "Failed to get charging status", e)
            -1
        }
    }

    private fun setIgnitionState(textView: TextView, value: Int) {
        when (value) {
            // lock
            1 -> textView.setText(R.string.lock)
            // OFF
            2 -> textView.setText(R.string.off)
            // ACC
            3 -> textView.setText(R.string.acc)
            // ON
            4 -> textView.setText(R.string.on)
            // START
            5 -> textView.setText(R.string.start)
        }
    }
}
