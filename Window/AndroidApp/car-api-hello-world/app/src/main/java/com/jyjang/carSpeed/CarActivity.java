package com.jyjang.carSpeed;

import android.Manifest;
import android.animation.ValueAnimator;
import android.car.Car;
import android.car.VehiclePropertyIds;
import android.car.hardware.CarPropertyConfig;
import android.car.hardware.CarPropertyValue;
import android.car.hardware.property.CarPropertyManager;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.PorterDuffColorFilter;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.example.carapihelloworld.R;
import com.github.anastr.speedviewlib.AwesomeSpeedometer;

import java.util.ArrayList;
import java.util.List;


public class CarActivity extends AppCompatActivity {

    private final int YELLOW = Color.parseColor("#FFFF00"); // 노란
    private final int WHITE = Color.parseColor("#FFFFFF"); // 하양 
    
    private static CarPropertyManager mCarPropertyManager;

    private ImageView chargePortConnectImage;
    private ImageView chargePortOpenImage;
    private ImageView autoParkingImage;

    private TextView parkGearImage;
    private TextView reverseGearImage;
    private TextView driveGearImage;
    private TextView neutralGearImage;

    private TextView speedTextView;
    private TextView ignitionTextView;

    private static  final  String TAG = "CarActivity";
    private  static  final  int PERMISSION_REQUEST_CODE = 100;

    public CarActivity() {
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        List<String> dangPermToRequest = checkDangerousPermissions();
        requestDangerousPermissions(dangPermToRequest);
        setContentView(R.layout.car_action_activity);


        chargePortOpenImage = findViewById(R.id.charge_port_open_image);
        chargePortConnectImage = findViewById(R.id.charge_port_connect_image);
        autoParkingImage = findViewById(R.id.auto_parking_image);

        parkGearImage = findViewById(R.id.park_gear_text);
        reverseGearImage = findViewById(R.id.reverse_gear_text);
        driveGearImage = findViewById(R.id.drive_gear_text);
        neutralGearImage = findViewById(R.id.neutral_gear_text);

//        speedTextView = findViewById(R.id.speed_text_view);
        ignitionTextView = findViewById(R.id.ignition_state_text);

        main();
    }

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

        if (checkSelfPermission(Car.PERMISSION_USE_REMOTE_ACCESS) != PackageManager.PERMISSION_GRANTED) {
            permissions.add(Car.PERMISSION_USE_REMOTE_ACCESS);
        }
        return permissions;
    }

    private void requestDangerousPermissions(List<String> permissions) {
        requestPermissions(permissions.toArray(new String[0]), PERMISSION_REQUEST_CODE);
    }
    private void initCarPropertyManager() {
        Car mCar = Car.createCar(this);

        mCarPropertyManager = (CarPropertyManager) mCar.getCarManager(Car.PROPERTY_SERVICE);
    }

    private void main(){
        initCarPropertyManager();

        for(CarPropertyConfig config : mCarPropertyManager.getPropertyList()){
            Log.d(TAG, String.valueOf(config.getPropertyId()));
        };
        Log.d(TAG, "CarPropertyConfig List Size : "+String.valueOf(mCarPropertyManager.getPropertyList().size()));

        registerCallback();
    }


    private void registerCallback(){
        //EV_CHARGE_PORT_OPEN
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "(EV_CHARGE_PORT_OPEN) Set " + propertyValue);
                setImageViewPropValue(chargePortOpenImage, (boolean) propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.EV_CHARGE_PORT_OPEN, CarPropertyManager.SENSOR_RATE_NORMAL);

        //EV_CHARGE_PORT_CONNECTED
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "is Change " + propertyValue);
                setImageViewPropValue(chargePortConnectImage, (boolean) propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.EV_CHARGE_PORT_CONNECTED, CarPropertyManager.SENSOR_RATE_NORMAL);

        //PARKING_BRAKE_AUTO_APPLY
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "(PARKING_BRAKE_AUTO_APPLY)is Change " + propertyValue);
                setImageViewPropValue(autoParkingImage, (boolean) propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.PARKING_BRAKE_AUTO_APPLY, CarPropertyManager.SENSOR_RATE_NORMAL);

        //GEAR_SELECTION
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "(GEAR_SELECTION)is Change " + propertyValue);
                setGearButtonColorFilter((Integer)propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.GEAR_SELECTION, CarPropertyManager.SENSOR_RATE_NORMAL);

        //PERF_VEHICLE_SPEED
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "(PERF_VEHICLE_SPEED)is Change " + propertyValue);
                AwesomeSpeedometer awesomeSpeedometer= (AwesomeSpeedometer) findViewById(R.id.awesomeSpeedometer);
                awesomeSpeedometer.speedTo((float)propertyValue);
//                setCarSpeedValue(speedTextView,(float)propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.PERF_VEHICLE_SPEED_DISPLAY, CarPropertyManager.SENSOR_RATE_NORMAL);

        //IGNITION_STATE
        mCarPropertyManager.registerCallback(new CarPropertyManager.CarPropertyEventCallback() {
            @Override
            public void onChangeEvent(CarPropertyValue carPropertyValue) {
                int propertyId = carPropertyValue.getPropertyId();
                Object propertyValue = carPropertyValue.getValue();
                Log.d(TAG, propertyId + "(IGNITION_STATE)is Change " + propertyValue);
                setIgnitionState(ignitionTextView, (Integer) propertyValue);
            }

            @Override
            public void onErrorEvent(int propId, int zone) {
                Log.e(TAG, "Error event for property ID: " + propId + ", zone: " + zone);
            }
        }, VehiclePropertyIds.IGNITION_STATE, CarPropertyManager.SENSOR_RATE_NORMAL);
    }


    public void setImageViewPropValue(ImageView imageView, boolean value){
        if(!value){
            int color = Color.parseColor("#00BFFF"); // 파란색
            PorterDuffColorFilter colorFilter = new PorterDuffColorFilter(color, PorterDuff.Mode.SRC_ATOP);
            imageView.setColorFilter(colorFilter);
            return;
        }
        imageView.setColorFilter(null);
    }


    public void setGearButtonColorFilter(int value){
        switch (value){
            //N
            case 1 :
                parkGearImage.setTextColor(WHITE);
                reverseGearImage.setTextColor(WHITE);
                driveGearImage.setTextColor(WHITE);
                neutralGearImage.setTextColor(YELLOW);
                break;
            //R
            case 2 :
                parkGearImage.setTextColor(WHITE);
                reverseGearImage.setTextColor(YELLOW);
                driveGearImage.setTextColor(WHITE);
                neutralGearImage.setTextColor(WHITE);
                break;
            //P
            case 4 :
                parkGearImage.setTextColor(YELLOW);
                reverseGearImage.setTextColor(WHITE);
                driveGearImage.setTextColor(WHITE);
                neutralGearImage.setTextColor(WHITE);
                break;
            //D
            case 8 :
                parkGearImage.setTextColor(WHITE);
                reverseGearImage.setTextColor(WHITE);
                driveGearImage.setTextColor(YELLOW);
                neutralGearImage.setTextColor(WHITE);
                break;
        }
    }

    public void setCarSpeedValue(TextView textView, float newValue) {
        String currentSpeedText = textView.getText().toString();
        int currentSpeed;

        try {
            currentSpeed = Integer.parseInt(currentSpeedText);
        } catch (NumberFormatException e) {
            currentSpeed = 0;
        }

        int newSpeed = (int) newValue;

        ValueAnimator animator = ValueAnimator.ofInt(currentSpeed, newSpeed);
        animator.setDuration(700);
        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator animation) {
                int animatedValue = (int) animation.getAnimatedValue();
                textView.setText(String.valueOf(animatedValue));
            }
        });
        animator.start();
    }

    public void setIgnitionState(TextView textView, int value){
        switch (value){
            //lock
            case 1 :
                textView.setText(R.string.lock);
                break;
            //OFF
            case 2 :
                textView.setText(R.string.off);
                break;
            //ACC
            case 3 :
                textView.setText(R.string.acc);
                break;
            //ON
            case 4 :
                textView.setText(R.string.on);
                break;
            //START
            case 5 :
                textView.setText(R.string.start);
                break;
        }

    }
}