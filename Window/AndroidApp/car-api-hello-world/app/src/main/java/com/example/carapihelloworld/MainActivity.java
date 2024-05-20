package com.example.carapihelloworld;

import android.Manifest;
import android.car.Car;
import android.car.VehiclePropertyIds;
import android.car.hardware.CarPropertyConfig;
import android.car.hardware.CarPropertyValue;
import android.car.hardware.property.CarInternalErrorException;
import android.car.hardware.property.CarPropertyManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.jyjang.carSpeed.GearActivity;

import java.util.ArrayList;
import java.util.List;

import vendor.nlab.vehicle.V1_0.VehicleProperty;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "Car Vhal Reader View";
    private static final int REQUEST_CODE_ASK_PERMISSIONS = 1;
    private String[] permissions = {Car.PERMISSION_SPEED, Car.PERMISSION_CONTROL_CAR_ENERGY};

    private static final int PERMISSION_REQUEST_CODE = 100;
    VehiclePropertyView mGearPropertyView;
    VehiclePropertyView mSpeedPropertyView;
    VehiclePropertyView mTirePressureView;



    private static CarPropertyManager mCarPropertyManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        checkAndRequestPermissions();
        // Request dangerous permissions only
        List<String> dangPermToRequest = checkDangerousPermissions();
        requestDangerousPermissions(dangPermToRequest);

        main();
        Button buttonOpenActivity = findViewById(R.id.move_view_button);
        buttonOpenActivity.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(MainActivity.this, GearActivity.class);
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (checkSelfPermission(permissions[0]) == PackageManager.PERMISSION_GRANTED) {
            // your code here
        } else {
            requestPermissions(permissions, 0);
        }
    }

    private void checkAndRequestPermissions() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission_group.SENSORS) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission_group.SENSORS}, PERMISSION_REQUEST_CODE);
        } else {
            Log.d(TAG, "SENSORS permission is already granted");
        }
    }

    private void main() {
        initCarPropertyManager();
        initGUI();

        for(CarPropertyConfig carPropertyConfig : mCarPropertyManager.getPropertyList()){
            Log.d(TAG, "carPropertyConfig : " + carPropertyConfig.getPropertyId());
        }

        registerCarPropertyManagerCBs();
    }

    @NonNull
    private List<String> checkDangerousPermissions() {
        List<String> permissions = new ArrayList<String>();

        if (checkSelfPermission(Manifest.permission.WRITE_SECURE_SETTINGS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Manifest.permission.WRITE_SECURE_SETTINGS);
        }

        if (checkSelfPermission(Manifest.permission.SET_DEBUG_APP) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Manifest.permission.SET_DEBUG_APP);
        }

        if (checkSelfPermission(Car.PERMISSION_CAR_INFO) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_CAR_INFO);
        }

        if (checkSelfPermission(Car.PERMISSION_CONTROL_DISPLAY_UNITS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_CONTROL_DISPLAY_UNITS);
        }

        if (checkSelfPermission(Car.PERMISSION_POWERTRAIN) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_POWERTRAIN);
        }

        if (checkSelfPermission(Car.PERMISSION_READ_DISPLAY_UNITS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_READ_DISPLAY_UNITS);
        }

        if (checkSelfPermission(Car.PERMISSION_SPEED) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_SPEED);
        }

        if (checkSelfPermission(Car.PERMISSION_ENERGY_PORTS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_ENERGY_PORTS);
        }

        if (checkSelfPermission(Car.PERMISSION_ENERGY) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_ENERGY);
        }




        return permissions;
    }

    private void requestDangerousPermissions(@NonNull List<String> permissions) {
        requestPermissions(permissions.toArray(new String[0]), REQUEST_CODE_ASK_PERMISSIONS);
    }

    private void initGUI() {
        setContentView(R.layout.activity_main);

        mGearPropertyView = findViewById(R.id.gear_property_view);

        mGearPropertyView.setPropId(VehiclePropertyIds.EV_CHARGE_PORT_OPEN)
                .setPropName("EV 충전 포트 연결 상태")
                .enableSetValue(value_to_set -> {
                    Log.d(TAG, "연결 상태 변경 : onEdit(" + value_to_set + ")");
                    CarPropertyConfig<?> gearPropConfig = mCarPropertyManager.getCarPropertyConfig(VehiclePropertyIds.GEAR_SELECTION);
                    if(gearPropConfig.getChangeMode() == CarPropertyConfig.VEHICLE_PROPERTY_ACCESS_WRITE ||
                            gearPropConfig.getChangeMode() == CarPropertyConfig.VEHICLE_PROPERTY_CHANGE_MODE_ONCHANGE ||
                            gearPropConfig.getChangeMode() == CarPropertyConfig.VEHICLE_PROPERTY_ACCESS_NONE ||
                            gearPropConfig.getChangeMode() == CarPropertyConfig.VEHICLE_PROPERTY_CHANGE_MODE_STATIC ||
                            gearPropConfig.getChangeMode() == CarPropertyConfig.VEHICLE_PROPERTY_ACCESS_READ_WRITE
                    ){
                        try{
                            mCarPropertyManager.setBooleanProperty(VehiclePropertyIds.EV_CHARGE_PORT_OPEN, 0, Boolean.parseBoolean(value_to_set));
                        } catch (SecurityException | IllegalArgumentException | CarInternalErrorException e) {
                            Log.e(TAG, "연결 상태 변경 : setProperty(), Exception: " + e.getMessage());
                        }
                    }
                });

        mSpeedPropertyView = findViewById(R.id.speed_property_view);
        mSpeedPropertyView.setPropId(VehiclePropertyIds.PERF_VEHICLE_SPEED)
                .setPropName("차량 속도 VHAL")
                .enableSetValue(value_to_set -> {
                    Log.d(TAG, "속도 변경 : setProperty(" + value_to_set + ")");
                    try{
                        mCarPropertyManager.setFloatProperty(VehiclePropertyIds.PERF_VEHICLE_SPEED, 0, Float.parseFloat(value_to_set));
                    } catch(SecurityException | IllegalArgumentException | CarInternalErrorException e){
                        Log.e(TAG, "속도 변경 : setProperty(), Exception: " + e.getMessage());
                    }
                });
    }

    private void initCarPropertyManager() {
        Car mCar = Car.createCar(this);
        mCarPropertyManager = (CarPropertyManager) mCar.getCarManager(Car.PROPERTY_SERVICE);
    }

    private void registerCarPropertyManagerCBs() {
        //GEAR
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                Log.d(TAG, "EV_CHARGE_PORT_OPEN: onChangeEvent(" + carPropertyValue.getValue() + ")");
                mGearPropertyView.setPropValue(String.valueOf(carPropertyValue.getValue()));
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.d(TAG, "EV_CHARGE_PORT_OPEN: onErrorEvent(" + propId + ", " + zone + ")");
            }

        }, VehiclePropertyIds.EV_CHARGE_PORT_OPEN, CarPropertyManager.SENSOR_RATE_NORMAL);

        //SPEED
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                Log.d(TAG, "PERF_VEHICLE_SPEED: onChangeEvent(" + carPropertyValue.getValue() + ")");
                mSpeedPropertyView.setPropValue(String.valueOf(carPropertyValue.getValue()));
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.d(TAG, "PERF_VEHICLE_SPEED: onErrorEvent(" + propId + ", " + zone + ")");
            }

        }, VehicleProperty.VENDOR_TEST_1S_COUNTER, CarPropertyManager.SENSOR_RATE_NORMAL);
    }

    public static CarPropertyManager getCarManager() {
        return mCarPropertyManager;
    }
}
