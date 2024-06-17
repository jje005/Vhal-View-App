package com.jyjang.carSpeed.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import com.example.carapihelloworld.R

class PropertyListAdapter (private val context: Context,  private val propertyList:  ArrayList<String>) : BaseAdapter() {
    override fun getCount(): Int {
        return propertyList.size
    }

    override fun getItem(position: Int): Any {
        return propertyList[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        val view: View = convertView ?: LayoutInflater.from(context).inflate(R.layout.list_item_property, parent, false)
        val propertyText = view.findViewById<TextView>(R.id.propertyText)
        val propertyNumber = view.findViewById<TextView>(R.id.propertyNumber)

        propertyText.text = propertyList[position]
        propertyNumber.text = (position + 1).toString()

        return view
    }
}