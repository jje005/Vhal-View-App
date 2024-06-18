package com.jyjang.carSpeed

import android.Manifest
import android.car.Car
import android.car.hardware.property.CarPropertyManager
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.viewpager2.widget.ViewPager2
import com.example.carapihelloworld.R
import com.google.android.material.tabs.TabLayout
import com.google.android.material.tabs.TabLayoutMediator
import com.jyjang.carSpeed.adapter.ToolbarStateAdapter
import com.jyjang.carSpeed.model.CarPropertyManagerSingleton

class MainActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "MainActivity"
        private const val PERMISSION_REQUEST_CODE = 200
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val tabLayout = findViewById<TabLayout>(R.id.tab_Table_View)
        val viewPager = findViewById<ViewPager2>(R.id.viewPager)

        viewPager.adapter = ToolbarStateAdapter(this)

        TabLayoutMediator(tabLayout, viewPager) { tab, position ->
            when (position) {
                0 -> {
                    tab.text = "ClusterView"
                    tab.contentDescription = "Cluster View"
                }
                1 -> {
                    tab.text = "VHAL Properties list"
                    tab.contentDescription = "Vhal List View"
                }
            }

        }.attach()

        val permissions = checkDangerousPermissions()
        requestDangerousPermissions(permissions)

    }


    private fun checkDangerousPermissions(): List<String> {
        val permissions = ArrayList<String>()

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

        if (checkSelfPermission(Car.PERMISSION_ENERGY) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_ENERGY)
        }

        return permissions
    }

    private fun requestDangerousPermissions(permissions: List<String>) {
        requestPermissions(permissions.toTypedArray(), PERMISSION_REQUEST_CODE)
    }

}
