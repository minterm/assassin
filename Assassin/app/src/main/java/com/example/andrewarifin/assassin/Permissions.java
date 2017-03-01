package com.example.andrewarifin.assassin;

import android.bluetooth.BluetoothAdapter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;
import android.widget.TextView;

import static android.R.id.button1;
import static android.R.id.button2;
import static android.R.id.message;


public class Permissions extends AppCompatActivity {
    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_permissions);


        if (!mBluetoothAdapter.isEnabled()) {
            TextView tv = (TextView) findViewById(R.id.button9);
            tv.setText("Enable");
            //mBluetoothAdapter.enable();
        }
        else {
            TextView tv = (TextView) findViewById(R.id.button9);
            tv.setText("Disable");
            //mBluetoothAdapter.disable();
        }

    }

    public void btbutton(View view){
        if (!mBluetoothAdapter.isEnabled()) {
            TextView tv = (TextView) findViewById(R.id.button9);
            tv.setText("Disable");
            mBluetoothAdapter.enable();
        }
        else {
            TextView tv = (TextView) findViewById(R.id.button9);
            tv.setText("Enable");
            mBluetoothAdapter.disable();
        }
    }

}
