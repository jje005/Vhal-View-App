package com.jyjang.carSpeed

import android.Manifest
import android.animation.ValueAnimator
import android.car.Car
import android.car.VehiclePropertyIds
import android.car.hardware.CarPropertyConfig
import android.car.hardware.CarPropertyValue
import android.car.hardware.property.CarPropertyManager
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.PorterDuff
import android.graphics.PorterDuffColorFilter
import android.os.Bundle
import android.util.Log
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.carapihelloworld.R
import com.github.anastr.speedviewlib.AwesomeSpeedometer

class CarActivity2 : AppCompatActivity() {

    private val YELLOW = Color.parseColor("#FFFF00")
    private val WHITE = Color.parseColor("#FFFFFF")

    private lateinit var mCarPropertyManager: CarPropertyManager

    private lateinit var chargePortConnectImage: ImageView
    private lateinit var chargePortOpenImage: ImageView
    private lateinit var autoParkingImage: ImageView

    private lateinit var parkGearImage: TextView
    private lateinit var reverseGearImage: TextView
    private lateinit var driveGearImage: TextView
    private lateinit var neutralGearImage: TextView

    private lateinit var ignitionTextView: TextView

    companion object {
        private const val TAG = "CarActivity"
        private const val PERMISSION_REQUEST_CODE = 100
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val dangPermToRequest = checkDangerousPermissions()
        requestDangerousPermissions(dangPermToRequest)
        setContentView(R.layout.car_action_activity)

        chargePortOpenImage = findViewById(R.id.charge_port_open_image)
        chargePortConnectImage = findViewById(R.id.charge_port_connect_image)
        autoParkingImage = findViewById(R.id.auto_parking_image)

        parkGearImage = findViewById(R.id.park_gear_text)
        reverseGearImage = findViewById(R.id.reverse_gear_text)
        driveGearImage = findViewById(R.id.drive_gear_text)
        neutralGearImage = findViewById(R.id.neutral_gear_text)

        ignitionTextView = findViewById(R.id.ignition_state_text)

        main()
    }

    private fun checkDangerousPermissions(): List<String> {
        val permissions = mutableListOf<String>()

        if (checkSelfPermission(Manifest.permission.WRITE_SECURE_SETTINGS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Manifest.permission.WRITE_SECURE_SETTINGS)
        }

        if (checkSelfPermission(Manifest.permission.SET_DEBUG_APP) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Manifest.permission.SET_DEBUG_APP)
        }

        if (checkSelfPermission(Car.PERMISSION_CAR_INFO) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_CAR_INFO)
        }

        if (checkSelfPermission(Car.PERMISSION_CONTROL_DISPLAY_UNITS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_CONTROL_DISPLAY_UNITS)
        }

        if (checkSelfPermission(Car.PERMISSION_POWERTRAIN) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_POWERTRAIN)
        }

        if (checkSelfPermission(Car.PERMISSION_READ_DISPLAY_UNITS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_READ_DISPLAY_UNITS)
        }

        if (checkSelfPermission(Car.PERMISSION_SPEED) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_SPEED)
        }

        if (checkSelfPermission(Car.PERMISSION_USE_REMOTE_ACCESS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_USE_REMOTE_ACCESS)
        }

        return permissions
    }

    private fun requestDangerousPermissions(permissions: List<String>) {
        requestPermissions(permissions.toTypedArray(), PERMISSION_REQUEST_CODE)
    }

    private fun initCarPropertyManager() {
        val mCar = Car.createCar(this)
        mCarPropertyManager = mCar.getCarManager(Car.PROPERTY_SERVICE) as CarPropertyManager
    }

    private fun main() {
        initCarPropertyManager()

        for (config in mCarPropertyManager.propertyList) {
            Log.d(TAG, config.propertyId.toString())
        }
        Log.d(TAG, "CarPropertyConfig List Size : ${mCarPropertyManager.propertyList.size}")

        registerCallback()
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
                Log.d(TAG, "$propertyId is Change $propertyValue")
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
                Log.d(TAG, "$propertyId (GEAR_SELECTION)is Change $propertyValue")
                setGearButtonColorFilter(propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.GEAR_SELECTION, CarPropertyManager.SENSOR_RATE_NORMAL)

        // PERF_VEHICLE_SPEED
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Float
                Log.d(TAG, "$propertyId (PERF_VEHICLE_SPEED)is Change $propertyValue")
                val awesomeSpeedometer = findViewById<AwesomeSpeedometer>(R.id.awesomeSpeedometer)
                awesomeSpeedometer.speedTo(propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.PERF_VEHICLE_SPEED, CarPropertyManager.SENSOR_RATE_NORMAL)

        // IGNITION_STATE
        mCarPropertyManager.registerCallback(object : CarPropertyManager.CarPropertyEventCallback {
            override fun onChangeEvent(carPropertyValue: CarPropertyValue<*>) {
                val propertyId = carPropertyValue.propertyId
                val propertyValue = carPropertyValue.value as Int
                Log.d(TAG, "$propertyId (IGNITION_STATE)is Change $propertyValue")
                setIgnitionState(ignitionTextView, propertyValue)
            }

            override fun onErrorEvent(propId: Int, zone: Int) {
                Log.e(TAG, "Error event for property ID: $propId, zone: $zone")
            }
        }, VehiclePropertyIds.IGNITION_STATE, CarPropertyManager.SENSOR_RATE_NORMAL)
    }

    private fun setImageViewPropValue(imageView: ImageView, value: Boolean) {
        if (!value) {
            val color = Color.parseColor("#FF0000")
            val colorFilter = PorterDuffColorFilter(color, PorterDuff.Mode.SRC_ATOP)
            imageView.colorFilter = colorFilter
            return
        }
        imageView.colorFilter = null
    }

    private fun setGearButtonColorFilter(value: Int) {
        when (value) {
            1 -> {
                parkGearImage.setTextColor(WHITE)
                reverseGearImage.setTextColor(WHITE)
                driveGearImage.setTextColor(WHITE)
                neutralGearImage.setTextColor(YELLOW)
            }
            2 -> {
                parkGearImage.setTextColor(WHITE)
                reverseGearImage.setTextColor(YELLOW)
                driveGearImage.setTextColor(WHITE)
                neutralGearImage.setTextColor(WHITE)
            }
            4 -> {
                parkGearImage.setTextColor(YELLOW)
                reverseGearImage.setTextColor(WHITE)
                driveGearImage.setTextColor(WHITE)
                neutralGearImage.setTextColor(WHITE)
            }
            8 -> {
                parkGearImage.setTextColor(WHITE)
                reverseGearImage.setTextColor(WHITE)
                driveGearImage.setTextColor(YELLOW)
                neutralGearImage.setTextColor(WHITE)
            }
        }
    }


    private fun setIgnitionState(textView: TextView, value: Int) {
        when (value) {
            1 -> textView.setText(R.string.lock)
            2 -> textView.setText(R.string.off)
            3 -> textView.setText(R.string.acc)
            4 -> textView.setText(R.string.on)
            5 -> textView.setText(R.string.start)
        }
    }
}
