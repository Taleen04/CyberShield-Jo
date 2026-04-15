import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

void shareResult(context) {
  showDialog(
    context: context,
    builder: (context) {
      return StatefulBuilder(
        builder: (context, setState) {
          return AlertDialog(
            backgroundColor: AppColors.backgroundColor,
            title: Text("High-Risk Threat Detected "),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text("Case ID: #CSJ-10234"),
                SizedBox(height: 5),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    "Risk Level: High ⚠️",
                    style: TextStyle(color: Colors.red),
                  ),
                ),
                SizedBox(height: 10),
                Text("Reported URL: https://phishingsite.example.com"),
                SizedBox(height: 20),
                ElevatedButton.icon(
                  icon: Icon(Icons.people),
                  label: Text("Alert Community"),
                  onPressed: () {
                    /* trigger in-app alert */
                  },
                ),
                ElevatedButton.icon(
                  icon: Icon(Icons.share),
                  label: Text("Share Externally"),
                  onPressed: () {
                    /* share_plus package */
                  },
                ),
                ElevatedButton.icon(
                  icon: Icon(Icons.business),
                  label: Text("Send to Cyber Crimes Unit"),
                  onPressed: () {
                    /* send to official API/email */
                  },
                ),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text("Done"),
              ),
            ],
          );
        },
      );
    },
  );
}
