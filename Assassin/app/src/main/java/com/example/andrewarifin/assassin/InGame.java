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
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Log;
import android.view.View;

import android.bluetooth.BluetoothAdapter;
import android.content.BroadcastReceiver;
import android.widget.Button;
import android.widget.Toast;
import android.widget.ListView;
import java.util.ArrayList;
import java.util.HashMap;

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
    private static InGame ins;
    int LOCATION_REQUEST;
    TextView targetInfo;
    Button assassinateBtn;
    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
    private ListView listView;
    private ArrayList<String> mDeviceList = new ArrayList<String>();
    String targetName;
    String gameId;
    String name;
    String tName;
    String url = "http://minterm.pythonanywhere.com/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        ins = this;
        Intent prevIntent = getIntent();
        gameId = prevIntent.getStringExtra("GAME ID");
        name = prevIntent.getStringExtra("NAME");
        Log.i("Test", gameId);
        Log.i("Test", name);

        super.onCreate(savedInstanceState);
        PackageManager pm  = this.getPackageManager();
        ComponentName componentName = new ComponentName(this, MyReceiver.class);
        pm.setComponentEnabledSetting(componentName,PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                PackageManager.DONT_KILL_APP);
        Context context = this.getApplicationContext();
        String apiUrl = url + "api/info?g_id=" + gameId + "&p_name=" + name;
//        Log.v("Test", "oncreate");

//        AlarmManager am = (AlarmManager)context.getSystemService(Context.ALARM_SERVICE);
        Intent intent = new Intent(context, MyReceiver.class);
        intent.putExtra("g_id", gameId);
        intent.putExtra("p_name", name);
        final LocationManager lm = (LocationManager) context.getSystemService(Context.LOCATION_SERVICE);
        final PendingIntent pi = PendingIntent.getBroadcast(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
//        am1!.setRepeating(AlarmManager.RTC_WAKEUP, System.currentTimeMillis(), 1000 * 5, pi);
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
        lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 1000 * 5, 0, pi);
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000 * 5, 0 , pi);


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
                        Log.i("INFO", response.toString());
                        try {
                            if(response.getString("t_loc") != null) {
                                targetInfo.setText(response.getString("t_mac"));
                                targetName = response.getString("t_mac");
                                tName = response.getString("t_name");
                                String locString = response.getString("t_loc");
                                TextView locText = (TextView) findViewById(R.id.locationName);
                                locText.setClickable(true);
                                locText.setMovementMethod(LinkMovementMethod.getInstance());
                                String locationURL = "<a href='http://maps.google.com/?q=" + locString + "'> Location </a>";
                                locText.setText(Html.fromHtml(locationURL));
                                TextView statusText = (TextView)findViewById(R.id.statusText);
                                int status = response.getInt("alive");
                                if(status == 1) {
                                    statusText.setText("Alive");
                                } else {
                                    statusText.setText("Dead");
                                    lm.removeUpdates(pi);
                                }
                            }
                        }
                        catch (JSONException e) {
                            Log.e("JSON Err", e.toString());
                        }
                        Log.v("Test", response.toString());
                    }

                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //TO DO Auto generated method stub
                        Log.e("Volley error", error.toString());
                    }
                });

        queue.add(jsObjRequest);

        assassinateBtn = (Button)findViewById(R.id.button2);
        assassinateBtn.setEnabled(false);
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
                //discovery finishes, dismiss progress dialog
                showToast("No more discovering");
            } else if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                //bluetooth device found
                BluetoothDevice device = (BluetoothDevice) intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                showToast("Found device " + device.getAddress());
                Log.i("TARGET NAME", targetName);
                if(targetName.equals(device.getAddress())) {
//                if(targetName.equals("2C:8A:72:03:B0:83")) {
//                    Log.i("test", );
                    assassinateBtn.setEnabled(true);
                }
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

    public static InGame getInstance() {
        return ins;
    }

    public void updateLocationText(final String t) {
        InGame.this.runOnUiThread(new Runnable() {
            public void run() {
                TextView locText = (TextView) findViewById(R.id.locationName);
                locText.setClickable(true);
                locText.setMovementMethod(LinkMovementMethod.getInstance());
                locText.setText(Html.fromHtml(t));
            }
        });
    }

    public void updateTargetText(final String t, final String name) {
        InGame.this.runOnUiThread(new Runnable() {
            public void run() {
                tName = name;
                TextView targetText = (TextView) findViewById(R.id.targetName);
                targetText.setText(t);
            }
        });
    }

    public void updateStatusText(final int status) {
        final Intent loseIntent = new Intent();
        loseIntent.setClass(this.getApplicationContext(), Lose.class);
        InGame.this.runOnUiThread(new Runnable() {
            public void run() {
                TextView statusText = (TextView)findViewById(R.id.statusText);
                if(status == 1) {
                    statusText.setText("Alive");
                } else {
                    statusText.setText("Dead");
                    startActivity(loseIntent);

                }
            }
        });
    }

    public void assassinate(View view) {
        Context context = this.getApplicationContext();
        Log.i("ass", "running assassinate");
        HashMap<String, String> params = new HashMap<String, String>();
        params.put("p_name", name);
        params.put("g_id", gameId);
        params.put("target", tName);

        RequestQueue queue = Volley.newRequestQueue(context);

        // POSTing player location
        JsonObjectRequest assassinate = new JsonObjectRequest
                (Request.Method.POST, url + "api/attack", new JSONObject(params), new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i("res", String.valueOf(response));
                    }

                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //TO DO Auto generated method stub
                        Log.e("Volley POST error", error.toString());
                    }
                });
        queue.add(assassinate);

    }
}