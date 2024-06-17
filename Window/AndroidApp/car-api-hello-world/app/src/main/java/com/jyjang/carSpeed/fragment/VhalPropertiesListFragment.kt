package com.jyjang.carSpeed.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.example.carapihelloworld.R

class VhalPropertiesListFragment : Fragment() {
    private var propertiesList: ArrayList<Any> = ArrayList()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_vhal_properties_list, container, false)
    }
}