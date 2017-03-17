package com.example.andrewarifin.assassin;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Log;
import android.widget.TextView;
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
import org.w3c.dom.Text;

import java.util.HashMap;

public class MyReceiver extends BroadcastReceiver {
    public MyReceiver() {
    }

    @Override
    public void onReceive(final Context context, Intent intent) {
        Log.v("alarm", "alarm received");
        Bundle b = intent.getExtras();
        String gameId = b.getString("g_id");
        String name = b.getString("p_name");
        try {
            if (b != null) {
                Location loc = (Location)b.get(android.location.LocationManager.KEY_LOCATION_CHANGED);

                if (loc != null) {
//                    Log.i("location", loc.toString());
//                    Toast toast = Toast.makeText(context, loc.toString(), Toast.LENGTH_SHORT);
//                    toast.show();
                    String lat = Double.toString(loc.getLatitude());
                    String lon = Double.toString(loc.getLongitude());
                    String locString = lat + "," + lon;

                    HashMap<String, String> params = new HashMap<String, String>();
                    params.put("p_name", name);
                    params.put("g_id", gameId);
                    params.put("loc", locString);

                    RequestQueue queue = Volley.newRequestQueue(context);
                    String url = "http://minterm.pythonanywhere.com/";

                    // POSTing player location
                    JsonObjectRequest postLocation = new JsonObjectRequest
                            (Request.Method.POST, url + "api/gps", new JSONObject(params), new Response.Listener<JSONObject>() {
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

                    //GETing target location
                    JsonObjectRequest getLocation = new JsonObjectRequest
                            (Request.Method.GET, url + "api/info?g_id=" + gameId + "&p_name=" + name, null, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
//                                        Log.i("GET response", response.toString());
                                        String locString = response.getString("t_loc");
                                        String locationURL = "<a href='http://maps.google.com/?q=" + locString + "'> Location </a>";
                                        InGame.getInstance().updateLocationText(locationURL);
                                        InGame.getInstance().updateStatusText(response.getInt("alive"));
                                        InGame.getInstance().updateTargetText(response.getString("t_mac"), response.getString("t_name"));
                                    }
                                    catch (JSONException e) {
                                        Log.e("JSON GET Err", e.toString());
                                    }
                                }

                            }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    //TO DO Auto generated method stub
                                    Log.e("Volley error", error.toString());
                                }
                            });

                    JsonObjectRequest getStatus = new JsonObjectRequest
                            (Request.Method.GET, url + "api/gameplay?g_id=" + gameId, null, new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
//                                        Log.i("GET response", response.toString());
                                        Integer status = response.getInt("status");
                                        if(status == 2) {
                                            Intent winIntent = new Intent();
                                            winIntent.putExtra("winner", response.getString("winner"));
                                            winIntent.setClass(context, Winner.class);
                                            winIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                                            context.startActivity(winIntent);
                                        }
                                    }
                                    catch (JSONException e) {
                                        Log.e("JSON GET Err", e.toString());
                                    }
                                }

                            }, new Response.ErrorListener() {
                                @Override
                                public void onErrorResponse(VolleyError error) {
                                    //TO DO Auto generated method stub
                                    Log.e("Volley error", error.toString());
                                }
                            });

                    queue.add(postLocation);
                    queue.add(getLocation);
                    queue.add(getStatus);
                }
            }
        }

        catch (Exception e) {
            Log.e("LocationReceiver", "Exception LocationReceiver" + e);
        }
    }

}
