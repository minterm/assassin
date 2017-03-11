package com.example.andrewarifin.assassin;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;

import org.json.JSONException;
import org.json.JSONObject;

public class MyReceiver extends BroadcastReceiver {
    public MyReceiver() {
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        Log.v("alarm", "alarm received");
        Bundle b = intent.getExtras();
        try {
            if (b != null) {
                Log.v("stuff", b.toString());
                Location loc = (Location)b.get(android.location.LocationManager.KEY_LOCATION_CHANGED);

                if (loc != null) {
                    Log.i("location", loc.toString());
                    Toast toast = Toast.makeText(context, loc.toString(), Toast.LENGTH_SHORT);
                    toast.show();
                    RequestQueue queue = Volley.newRequestQueue(context);
                    String url = "https://jsonplaceholder.typicode.com/posts/";

                    JsonObjectRequest jsObjRequest = new JsonObjectRequest
                            (Request.Method.POST, url, null, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
//                                    Log.i("res", String.valueOf(response));
                                    try {
                                        Log.i("res", String.valueOf(response.getString("id")));
                                    } catch (JSONException e){
                                        Log.e("err", "json err" + e);
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
            }
        }

        catch (Exception e) {
            Log.e("LocationReceiver", "Exception LocationReceiver" + e);
        }
    }

    public class NetworkAccess extends AsyncTask<Context, Void, Void> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Log.i("async", "pre-executing lol");
        }

        @Override
        protected Void doInBackground(Context... params) {
            RequestQueue queue = Volley.newRequestQueue(params[0]);
            String url = "https://jsonplaceholder.typicode.com/posts/";

            JsonObjectRequest jsObjRequest = new JsonObjectRequest
                    (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            Log.i("res", String.valueOf(response));
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

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            Log.i("request", "done");
        }

        protected void onProgressUpdate(Void... values) {}

    }
}
