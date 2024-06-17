package com.jyjang.carSpeed.fragment

import android.car.hardware.property.CarPropertyManager
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.appcompat.widget.SearchView
import androidx.fragment.app.Fragment
import com.example.carapihelloworld.R
import com.example.carapihelloworld.R.*
import com.jyjang.carSpeed.adapter.PropertyListAdapter
import com.jyjang.carSpeed.model.CarPropertyManagerSingleton

class VhalPropertiesListFragment : Fragment() {
    private lateinit var mCarPropertyManager: CarPropertyManager
    private var propertiesList: ArrayList<String> = ArrayList()
    private lateinit var listView : ListView
    private lateinit var searchView: SearchView

    companion object {
        private const val TAG = "VhalPropertiesListFragment"
        private const val PERMISSION_REQUEST_CODE = 100
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(layout.fragment_vhal_properties_list, container, false)

        listView = view.findViewById(R.id.property_list_view)
        searchView = view.findViewById(R.id.property_search_view)

        initPropertiesData()
        return view
    }

    private fun initPropertiesData() {
        mCarPropertyManager =  CarPropertyManagerSingleton.getInstance(requireContext()).carPropertyManager
        if (mCarPropertyManager == null) {
            Log.d(TAG, "CarPropertyManager is Null")
            return
        }

        for (config in mCarPropertyManager.propertyList) {
            Log.d(TAG, "Property :  " + config)
            propertiesList.add(config.toString())
        }

        val propertyAdapter = PropertyListAdapter(requireContext(), propertiesList)
        listView.adapter = propertyAdapter
    }
}