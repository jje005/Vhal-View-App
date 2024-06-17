package com.jyjang.carSpeed.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Filter
import android.widget.Filterable
import android.widget.TextView
import android.widget.Toast
import com.example.carapihelloworld.R

class PropertyListAdapter (private val context: Context,  private val propertyIdList:  ArrayList<String>, private val propertyNameList:ArrayList<String> ) : BaseAdapter(), Filterable {
    private var filteredPropertyIdList: ArrayList<String> = propertyIdList
    private var filteredPropertyNameList: ArrayList<String> = propertyNameList
    override fun getCount(): Int {
        return filteredPropertyIdList.size
    }

    override fun getItem(position: Int): Any {
        return filteredPropertyIdList[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        val view: View = convertView ?: LayoutInflater.from(context).inflate(R.layout.list_item_property, parent, false)
        val propertyIdText = view.findViewById<TextView>(R.id.property_id_Text)
        val propertyNameText = view.findViewById<TextView>(R.id.property_name_Text)
        val propertyNumber = view.findViewById<TextView>(R.id.propertyNumber)

        propertyIdText.text = filteredPropertyIdList[position]
        propertyNameText.text = filteredPropertyNameList[position]
        propertyNumber.text = (position + 1).toString()

        return view
    }

    override fun getFilter(): Filter {
        return object : Filter() {
            override fun performFiltering(charSequence: CharSequence?): FilterResults {
                val charString = charSequence?.toString() ?: ""
                val filteredIds = ArrayList<String>()
                val filteredNames = ArrayList<String>()

                if (charString.isEmpty()) {
                    filteredIds.addAll(propertyIdList)
                    filteredNames.addAll(propertyNameList)
                } else {
                    for (i in propertyNameList.indices) {
                        if (propertyIdList[i].contains(charString, true) || propertyNameList[i].contains(charString, true)) {
                            filteredIds.add(propertyIdList[i])
                            filteredNames.add(propertyNameList[i])
                        }
                    }

                }
                val filterResults = FilterResults()
                filterResults.values = Pair(filteredIds, filteredNames)
                return filterResults
            }

            override fun publishResults(charSequence: CharSequence?, filterResults: FilterResults?) {
                val resultPair = filterResults?.values as Pair<ArrayList<String>, ArrayList<String>>
                filteredPropertyIdList = resultPair.first
                filteredPropertyNameList = resultPair.second
                notifyDataSetChanged()
            }
        }
    }
}