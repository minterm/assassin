package com.example.andrewarifin.assassin;

import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class Winner extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Intent i = getIntent();
        super.onCreate(savedInstanceState);
        PackageManager pm  = this.getPackageManager();
        ComponentName componentName = new ComponentName(this, MyReceiver.class);
        pm.setComponentEnabledSetting(componentName,PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP);
        setContentView(R.layout.activity_winner);
        TextView winner = (TextView)findViewById(R.id.textView6);
        String winnerName = i.getStringExtra("winner");
        winner.setText(winnerName);
    }

    public void backToMain(View view){
        //startActivity(new Intent(Winner.this, MainActivity.class));
        finish();
    }
}
