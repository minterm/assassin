package com.example.andrewarifin.assassin;


import android.bluetooth.BluetoothAdapter;

import android.content.Context;
import android.content.pm.PackageManager;

import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.support.annotation.MainThread;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.content.Intent;
import android.widget.EditText;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;

public class MainActivity extends AppCompatActivity {
    EditText idInput;
    EditText nameInput;
    private static final int LOCATION_REQUEST = 0;
    String apiURL = "http://a8b934bf.ngrok.io/api/join";

    BluetoothAdapter mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);


//        if (mBluetoothAdapter == null)
//        {
//            //no bluetooth available
//            startActivity(new Intent(MainActivity.this, cannotPlay.class));
//        }
//
//        if (!mBluetoothAdapter.isEnabled()) {
//            //mBluetoothAdapter.enable();
//            startActivity(new Intent(MainActivity.this, Permissions.class));
//        }


        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            Log.e("Location err", "permission failed");
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, LOCATION_REQUEST);
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           String permissions[], int[] grantResults) {
        switch (requestCode) {
            case LOCATION_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {

                    // permission was granted, yay! Do the
                    // contacts-related task you need to do.

                } else {

                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.
                }
                return;
            }

            // other 'case' lines to check for other
            // permissions this app might request
        }

    }

    public void joinAGame(View view){
        idInput = (EditText)findViewById(R.id.textView7); // get game id input
        nameInput = (EditText)findViewById(R.id.nameInput); // get name input

        String gameVal = idInput.getText().toString();
        String nameVal = nameInput.getText().toString();

        String macAddress = android.provider.Settings.Secure.getString(getContentResolver(), "bluetooth_address");

        Intent intent = new Intent(MainActivity.this, InGame.class);
        intent.putExtra("GAME ID", gameVal);
        intent.putExtra("NAME", nameVal);
        intent.putExtra("MAC ADDRESS", macAddress);

        HashMap<String, String> params = new HashMap<String, String>();
        params.put("p_name", nameVal);
        params.put("g_id", gameVal);
        params.put("mac", macAddress);
        params.put("loc", null);

        RequestQueue queue = Volley.newRequestQueue(this);

        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.POST, apiURL, new JSONObject(params), new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        Log.i("JOIN", response.toString());
//                        try {
//                            targetInfo.setText(response.getString("userId"));
//                        }
//                        catch (JSONException e) {
//                            Log.e("JSON Err", e.toString());
//                        }
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
        startActivity(intent);
    }

    public void goToWin(View view){
        startActivity(new Intent(MainActivity.this, Winner.class));
    }
    public void goToLose(View view){
        startActivity(new Intent(MainActivity.this, Lose.class));
    }
    public void goToBTSettings(View view) { startActivity(new Intent(MainActivity.this, Permissions.class)); }
}

