package com.example.andrewarifin.assassin;

import android.app.Service;
import android.app.job.JobParameters;
import android.app.job.JobService;
import android.app.job.JobScheduler;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;

public class LocationService extends JobService {
    private static final String TAG = "LocationService";

    @Override
    public boolean onStartJob(JobParameters params) {
        Log.i(TAG, "on start job:" + params.getJobId());
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) {
        return true;
    }
}
