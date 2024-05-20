package com.jyjang.carSpeed.ui;

import android.annotation.SuppressLint;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.icu.number.Scale;
import android.os.Bundle;
import android.util.AttributeSet;
import android.view.View;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.example.carapihelloworld.R;

public class SpeedometerView extends View {
    private static final String TAG = "SpeedometerView";
    private final String kmText = "m/s"; // 중심에 표시할 텍스트

    public SpeedometerView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    public SpeedometerView(Context context) {
        super(context);
    }

    protected void onDraw(@NonNull Canvas canvas){
        super.onDraw(canvas);
        @SuppressLint("DrawAllocation") Paint pnt = new Paint();
        pnt.setStrokeWidth(10f);
        pnt.setColor(Color.parseColor("#FF6495ED"));
        pnt.setStyle(Paint.Style.STROKE);
        @SuppressLint("DrawAllocation") RectF rect = new RectF();
        rect.set(10, 10, 450, 450);



        @SuppressLint("DrawAllocation") Paint textPnt = new Paint();
        textPnt.setStrokeWidth(4f);
        textPnt.setColor(Color.WHITE);
//        textPnt.setColor(Color.parseColor("#FFF8F8FF"));
        textPnt.setStyle(Paint.Style.FILL);
        canvas.drawArc(rect, 150, 240, false, pnt);
       pnt.setStrokeWidth(2f);
        pnt.setColor(Color.parseColor("#FF6495ED"));
        float radius = (rect.right - rect.left) / 2;
        float centerX = rect.centerX();
        float centerY = rect.centerY();
        float angleStep = 5;
        for (float angle = 0; angle <= 360; angle += angleStep) {
            float startX = centerX + (float) Math.cos(Math.toRadians(angle - 90)) * radius;
            float startY = centerY + (float) Math.sin(Math.toRadians(angle - 90)) * radius;
            float endX = centerX + (float) Math.cos(Math.toRadians(angle - 90)) * (radius - 20);
            float endY = centerY + (float) Math.sin(Math.toRadians(angle - 90)) * (radius - 20);

            if(angle>120 && angle<240){
                continue;
            } else if (angle%20 == 0 && angle >240 ) {
                endX = centerX + (float) Math.cos(Math.toRadians(angle - 90)) * (radius - 40);
                endY = centerY + (float) Math.sin(Math.toRadians(angle - 90)) * (radius - 40);
                canvas.drawLine(startX, startY, endX, endY, pnt);
                if(angle == 360){
                    canvas.drawText(String.valueOf(angle-260), endX-15, endY+15, textPnt);
                    continue;
                }
                canvas.drawText(String.valueOf(angle-260), endX+5, endY+5, textPnt);
            } else if(angle%20 == 0 && angle <120 && angle != 0){
                endX = centerX + (float) Math.cos(Math.toRadians(angle - 90)) * (radius - 40);
                endY = centerY + (float) Math.sin(Math.toRadians(angle - 90)) * (radius - 40);
                canvas.drawLine(startX, startY, endX, endY, pnt);
                canvas.drawText(String.valueOf(angle+100), endX-35, endY+5, textPnt);
            }

            canvas.drawLine(startX, startY, endX, endY, pnt);

        }

        Rect textBounds = new Rect();
        Paint kmTextPnt = new Paint();

        kmTextPnt.getTextBounds(kmText, 0, Integer.parseInt(String.valueOf(kmText.length())), textBounds);
        kmTextPnt.setTextSize(32);
        kmTextPnt.setColor(Color.WHITE);


        float textWidth = kmTextPnt.measureText(kmText);
        float textHeight = textBounds.height();
        float textX = centerX - textWidth / 2;
        float textY = centerY + textHeight / 2;


        canvas.drawText(kmText, textX+5, textY, kmTextPnt);

    }
}