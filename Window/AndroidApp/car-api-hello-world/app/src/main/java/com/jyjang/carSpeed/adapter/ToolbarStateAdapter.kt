package com.jyjang.carSpeed.adapter

import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.viewpager2.adapter.FragmentStateAdapter
import com.jyjang.carSpeed.ClusterViewFragment
import com.jyjang.carSpeed.fragment.VhalPropertiesListFragment

class ToolbarStateAdapter(fragmentActivity: FragmentActivity) : FragmentStateAdapter(fragmentActivity) {

    override fun createFragment(position: Int): Fragment {
        return when (position) {
            0 -> ClusterViewFragment()
            1 -> VhalPropertiesListFragment()
            else -> Fragment()
        }
    }

    override fun getItemCount(): Int {
        return 2 // Number of tabs
    }
}