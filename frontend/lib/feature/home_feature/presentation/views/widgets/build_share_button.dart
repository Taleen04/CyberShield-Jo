import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/feature/submit_report.dart/presentation/views/submit_report.dart';
import 'package:flutter/material.dart';

Widget buildReportButton(BuildContext context) {
  return Padding(
    padding: const EdgeInsets.all(20.0),
    child: SizedBox(
      width: double.infinity,
      child: DecoratedBox(
        decoration: BoxDecoration(
          border: Border.all(color: AppColors.whiteColor),
          borderRadius: BorderRadius.circular(14),
        ),
        child: ElevatedButton.icon(
          onPressed: () {
            submitReport(context);
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
          icon: Icon(Icons.flag_rounded, color: AppColors.redColor, size: 18),
          label: Text(
            'Share this threat',
            style: TextStyle(
              color: AppColors.whiteColor,
              fontSize: 15,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    ),
  );
}
