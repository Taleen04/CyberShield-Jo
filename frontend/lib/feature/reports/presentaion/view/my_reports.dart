import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:cyper_shield_jo/feature/reports/presentaion/view/widgets/build_report_details.dart';
import 'package:flutter/material.dart';

class MyReports extends StatelessWidget {
  const MyReports({super.key});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    double horizontalMargin = screenWidth < 600 ? 16 : 20;
    double containerPadding = screenWidth < 600 ? 12 : 16;
    double textFont = screenWidth < 600 ? 14 : 18;
    double spacingHeight = screenWidth < 600 ? 12 : 16;
    double bottomSpacing = screenWidth < 600 ? 20 : 60;

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(18.0),
              child: Text(
                "My Reports",
                style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
              ),
            ),
            ReportDetails(
              containerPadding: containerPadding,
              horizontalMargin: horizontalMargin,
              spacingHeight: spacingHeight,
              textFont: textFont,
              bottomSpacing: bottomSpacing,
              title: "arabibank-secure.xyz",
              type: "URL.HTTPS fake",
              percentage: "61%",
            ),
            SizedBox(height: responsiveHeight(context, 20)),
            ReportDetails(
              containerPadding: containerPadding,
              horizontalMargin: horizontalMargin,
              spacingHeight: spacingHeight,
              textFont: textFont,
              bottomSpacing: bottomSpacing,
              title: "arabibank-secure.xyz",
              type: "URL.HTTPS fake",
              percentage: "80%",
            ),
          ],
        ),
      ),
    );
  }
}
