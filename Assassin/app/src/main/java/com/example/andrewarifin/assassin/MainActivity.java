package com.example.andrewarifin.assassin;

import android.support.annotation.MainThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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
}

