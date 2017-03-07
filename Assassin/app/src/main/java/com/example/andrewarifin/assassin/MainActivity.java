package com.example.andrewarifin.assassin;

import android.support.annotation.MainThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.content.Intent;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {
    EditText idInput;
    EditText nameInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void joinAGame(View view){
        idInput = (EditText)findViewById(R.id.textView7); // get game id input
        nameInput = (EditText)findViewById(R.id.nameInput); // get name input

        String gameVal = idInput.getText().toString();
        String nameVal = nameInput.getText().toString();

        Intent intent = new Intent(MainActivity.this, InGame.class);
        intent.putExtra("GAME ID", gameVal);
        intent.putExtra("NAME", nameVal);

        startActivity(intent);
    }

    public void goToWin(View view){
        startActivity(new Intent(MainActivity.this, Winner.class));
    }
    public void goToLose(View view){
        startActivity(new Intent(MainActivity.this, Lose.class));
    }
}

