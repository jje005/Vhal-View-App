package com.jyjang.carSpeed.model

import android.car.Car
import android.car.hardware.property.CarPropertyManager
import android.content.Context
import kotlin.concurrent.Volatile

class CarPropertyManagerSingleton private constructor(context: Context) {
    val carPropertyManager : CarPropertyManager

    init {
        val car = Car.createCar(context)
        carPropertyManager = car.getCarManager(Car.PROPERTY_SERVICE) as CarPropertyManager
    }

    companion object {
        @Volatile
        private var INSTANCE: CarPropertyManagerSingleton? = null

        fun getInstance(context: Context): CarPropertyManagerSingleton{
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: CarPropertyManagerSingleton(context.applicationContext).also  { INSTANCE = it }
            }
        }
    }
}