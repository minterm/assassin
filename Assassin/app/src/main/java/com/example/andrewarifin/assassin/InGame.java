package com.example.andrewarifin.assassin;

import android.app.job.JobInfo;
import android.app.job.JobScheduler;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
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
    LocationService locationService;
    private static int jobId = 0;

    TextView targetInfo;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        String apiUrl = "https://jsonplaceholder.typicode.com/posts/1";
        Log.v("Test", "oncreate");

        ComponentName mServiceComponent = new ComponentName(this, LocationService.class);
        Log.v("SERVICE", mServiceComponent.toString());
        JobInfo.Builder builder = new JobInfo.Builder(jobId++, mServiceComponent);
        Log.i("SERVICE", String.valueOf(JobInfo.getMinPeriodMillis()));
        builder.setPeriodic(3 * 1000);
        builder.setTriggerContentMaxDelay(2000);

        JobScheduler jobScheduler = (JobScheduler) getApplication().getSystemService(Context.JOB_SCHEDULER_SERVICE);
        jobScheduler.schedule(builder.build());

        RequestQueue queue = Volley.newRequestQueue(this);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_in_game);

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
        startActivity(new Intent(InGame.this, MainActivity.class));
    }
}
