import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:flutter/material.dart';

void submitReport(context) {
  String? selectedType;
  bool isChecked = false;

  showDialog(
    context: context,
    builder: (context) {
      final screenWidth = MediaQuery.of(context).size.width;

      double textFieldPadding = screenWidth < 600 ? 16 : 40;
      double spacing = screenWidth < 600 ? 12 : 20;
      double textFont = screenWidth < 600 ? 14 : 16;
      double titleFont = screenWidth < 600 ? 16 : 20;

      return SingleChildScrollView(
        child: StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              backgroundColor: AppColors.surfaceColor,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              title: Text(
                "Report this threat",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: titleFont,
                ),
              ),
              content: ConstrainedBox(
                constraints: BoxConstraints(maxWidth: 500),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      padding: EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        shape: BoxShape.rectangle,
                        color: AppColors.redColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        "80% of reported threats are scams",
                        style: TextStyle(color: AppColors.redColor),
                      ),
                    ),
                    SizedBox(height: spacing),
                    Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        "Choose the type of threat",
                        style: TextStyle(fontSize: textFont),
                      ),
                    ),
                    DropdownButton<String>(
                      value: selectedType,
                      isExpanded: true,
                      items: const [
                        DropdownMenuItem(
                          value: "SMS Message",
                          child: Text("SMS Message"),
                        ),
                        DropdownMenuItem(
                          value: "Suspicious Link",
                          child: Text("Suspicious Link"),
                        ),
                        DropdownMenuItem(
                          value: "Suspicious Call",
                          child: Text("Suspicious Call"),
                        ),
                      ],
                      onChanged: (value) {
                        setState(() {
                          selectedType = value!;
                        });
                      },
                    ),
                    SizedBox(height: spacing),
                    TextField(
                      maxLines: 5,
                      cursorColor: AppColors.grayColor,
                      decoration: InputDecoration(
                        hintText: "Notes....",
                        hintStyle: TextStyle(
                          color: AppColors.grayColor.withOpacity(0.30),
                          fontSize: textFont,
                        ),
                        filled: true,
                        fillColor: AppColors.gray2Color,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(
                            color: AppColors.primaryColor.withOpacity(0.07),
                          ),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(
                            color: AppColors.primaryColor.withOpacity(0.07),
                          ),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide(
                            color: AppColors.primaryColor.withOpacity(0.07),
                          ),
                        ),
                        contentPadding: EdgeInsets.all(textFieldPadding),
                      ),
                    ),
                    SizedBox(height: spacing),
                    CheckboxListTile(
                      controlAffinity: ListTileControlAffinity.leading,
                      title: Text(
                        "Submit the report anonymously",
                        style: TextStyle(fontSize: textFont),
                      ),
                      value: isChecked,
                      onChanged: (value) {
                        setState(() {
                          isChecked = value!;
                        });
                      },
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: Text(
                    "Cancel",
                    style: TextStyle(color: AppColors.redColor),
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    print(selectedType); // TODO: send report
                    Navigator.pop(context);
                  },
                  child: Text(
                    "Send 🚨",
                    style: TextStyle(color: AppColors.whiteColor),
                  ),
                ),
              ],
            );
          },
        ),
      );
    },
  );
}
