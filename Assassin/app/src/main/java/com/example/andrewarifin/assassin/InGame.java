package com.example.andrewarifin.assassin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class InGame extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_in_game);
    }

    public void backToMain(View view){
        startActivity(new Intent(InGame.this, MainActivity.class));
    }
}
