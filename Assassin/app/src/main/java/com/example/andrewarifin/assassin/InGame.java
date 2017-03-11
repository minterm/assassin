package com.example.andrewarifin.assassin;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.app.job.JobInfo;
import android.app.job.JobScheduler;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;

import android.content.Context;
import android.bluetooth.BluetoothDevice;
import android.content.IntentFilter;

import android.content.pm.PackageManager;
import android.location.LocationManager;
import android.support.v4.app.ActivityCompat;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import android.bluetooth.BluetoothAdapter;
import android.content.BroadcastReceiver;
import android.widget.Toast;
import android.widget.ListView;
import java.util.ArrayList;
import android.support.v4.app.ActivityCompat;
import android.Manifest;


import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class InGame extends AppCompatActivity {
    int LOCATION_REQUEST;
    TextView targetInfo;
    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    private ListView listView;
    private ArrayList<String> mDeviceList = new ArrayList<String>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Context context = this.getApplicationContext();
        String apiUrl = "https://jsonplaceholder.typicode.com/posts/1";
        Log.v("Test", "oncreate");

//        AlarmManager am = (AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        Intent intent = new Intent(context, MyReceiver.class);
        LocationManager lm = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
        PendingIntent pi = PendingIntent.getBroadcast(context, 0, intent, 0);
//        am.setRepeating(AlarmManager.RTC_WAKEUP, System.currentTimeMillis(), 1000 * 5, pi);
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.e("Location err", "permission failed");
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, LOCATION_REQUEST);
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
        }
        lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 5000, 0, pi);
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 0, pi);


        RequestQueue queue = Volley.newRequestQueue(this);

        setContentView(R.layout.activity_in_game);


        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        registerReceiver(mReceiver, filter);

        targetInfo = (TextView) findViewById(R.id.targetName);

        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.GET, apiUrl, null, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            targetInfo.setText(response.getString("userId"));
                        }
                        catch (JSONException e) {
                            Log.e("JSON Err", e.toString());
                        }
//                        Log.v("Test", response.toString());
                    }

                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //TO DO Auto generated method stub
                        Log.e("Volley error", error.toString());
                    }
                });

        queue.add(jsObjRequest);


    }

    public void backToMain(View view){
        //startActivity(new Intent(InGame.this, MainActivity.class));
        finish();
    }

    public void refresh(View view){
        int MY_PERMISSIONS_REQUEST_ACCESS_COARSE_LOCATION = 1;
        ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                MY_PERMISSIONS_REQUEST_ACCESS_COARSE_LOCATION);
        mBluetoothAdapter.startDiscovery();
    }

    private final BroadcastReceiver mReceiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();

            if (BluetoothAdapter.ACTION_DISCOVERY_STARTED.equals(action)) {
                //discovery starts, we can show progress dialog or perform other tasks
                showToast("Discovery started");
            } else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                //discovery finishes, dismis progress dialog
                showToast("No more discovering");
            } else if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                //bluetooth device found
                BluetoothDevice device = (BluetoothDevice) intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

                showToast("Found device " + device.getAddress());
                //showToast("WOOOHOOO");
            }
        }
    };

    @Override
    public void onDestroy() {
        unregisterReceiver(mReceiver);

        super.onDestroy();
    }

    private void showToast(String message) {
        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
}