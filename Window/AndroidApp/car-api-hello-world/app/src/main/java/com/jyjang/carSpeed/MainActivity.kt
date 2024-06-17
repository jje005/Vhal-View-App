package com.jyjang.carSpeed

import android.car.hardware.property.CarPropertyManager
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
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
    }

}
