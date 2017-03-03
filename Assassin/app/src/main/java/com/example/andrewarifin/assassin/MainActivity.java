package com.example.andrewarifin.assassin;

import android.bluetooth.BluetoothAdapter;
import android.support.annotation.MainThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;

public class MainActivity extends AppCompatActivity {

    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        if (mBluetoothAdapter == null)
        {
            //no bluetooth available
            startActivity(new Intent(MainActivity.this, cannotPlay.class));
        }

        if (!mBluetoothAdapter.isEnabled()) {
            //mBluetoothAdapter.enable();
            startActivity(new Intent(MainActivity.this, Permissions.class));
        }

    }

    public void joinAGame(View view){
        startActivity(new Intent(MainActivity.this, InGame.class));
    }

    public void goToWin(View view){
        startActivity(new Intent(MainActivity.this, Winner.class));
    }
    public void goToLose(View view){
        startActivity(new Intent(MainActivity.this, Lose.class));
    }
    public void goToBTSettings(View view) { startActivity(new Intent(MainActivity.this, Permissions.class)); }
}

