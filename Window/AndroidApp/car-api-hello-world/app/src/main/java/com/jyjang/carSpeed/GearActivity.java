package com.jyjang.carSpeed;

import android.car.Car;
import android.car.hardware.CarPropertyValue;
import android.car.hardware.property.CarPropertyManager;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.carapihelloworld.MainActivity;
import com.example.carapihelloworld.R;

import java.util.HashMap;
import java.util.Map;

public class GearActivity extends AppCompatActivity {

    private static final String TAG = "GearActivity";
    private CarPropertyManager carPropertyManager;

    private static final String GEAR_UNKNOWN = "GEAR_UNKNOWN";
    private static final Map<Integer, String> VEHICLE_GEARS = new HashMap<Integer, String>() {{
        put(0x0000, GEAR_UNKNOWN);
        put(0x0001, "GEAR_NEUTRAL");
        put(0x0002, "GEAR_REVERSE");
        put(0x0004, "GEAR_PARK");
        put(0x0008, "GEAR_DRIVE");
    }};

    private TextView currentGearTextView;
    private Car car;
    private int selectedGear = 0;

    public GearActivity() {
    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.gearactivity);
        carPropertyManager = MainActivity.getCarManager();

        currentGearTextView = findViewById(R.id.currentGearTextView);
        Button buttonNeutral = findViewById(R.id.buttonNeutral);
        Button buttonReverse = findViewById(R.id.buttonReverse);
        Button buttonPark = findViewById(R.id.buttonPark);
        Button buttonDrive = findViewById(R.id.buttonDrive);


        buttonNeutral.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedGear = 0x0001;
                sendGearCallback();
            }
        });

        buttonReverse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedGear = 0x0002;
                sendGearCallback();
            }
        });

        buttonPark.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedGear = 0x0004;
                sendGearCallback();
            }
        });

        buttonDrive.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                selectedGear = 0x0008;
                sendGearCallback();
            }
        });

        carPropertyManager.registerCallback(
                carPropertyListener,
                android.car.VehiclePropertyIds.CURRENT_GEAR,
                CarPropertyManager.SENSOR_RATE_ONCHANGE
        );
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
//        car.disconnect();
    }

    private void sendGearCallback() {
        CarPropertyValue<Object> gearPropertyValue = carPropertyManager.getProperty(289408000, 0);
        carPropertyListener.onChangeEvent(gearPropertyValue);
    }

    private final CarPropertyManager.CarPropertyEventCallback carPropertyListener =
            new CarPropertyManager.CarPropertyEventCallback() {
                @Override
                public void onChangeEvent(CarPropertyValue carPropertyValue) {
                    if (carPropertyValue != null) {
                        Log.d(TAG, "Received on changed car property event");
                        Object value = carPropertyValue.getValue();
                        if (value instanceof Integer) {
                            int gearValue = (int) value;
                            currentGearTextView.setText(VEHICLE_GEARS.get(selectedGear));
                        } else {
                            Log.e(TAG, "Unexpected value type or null value in CarPropertyValue");
                        }
                    } else {
                        Log.e(TAG, "Received null CarPropertyValue");
                    }
                }

                @Override
                public void onErrorEvent(int propId, int zone) {
                    Log.w(TAG, "Received error car property event, propId=" + propId);
                }
            };
}
