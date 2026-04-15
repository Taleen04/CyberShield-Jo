import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_analyze_button.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_analyze_tab.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_box_result.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_report_button.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/build_top_bar.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/recent_checks.dart';
import 'package:cyper_shield_jo/feature/submit_report.dart/presentation/views/submit_report.dart';
import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        buildTopBar(),
        SizedBox(height: 20),
        Expanded(
          child: SingleChildScrollView(
            child: Column(
              children: [
                BuildAnalyzeTab(),
                SizedBox(height: 20),
                buildAnalyzeButton(),
                SizedBox(height: 20),
                BuildBoxResult(),
                SizedBox(height: 20),
                Row(
                  children: [
                    Expanded(
                      child: buildCustomButton(context, "Report", () {
                        submitReport(context);
                      }),
                    ),
                    SizedBox(width: 10),
                    Expanded(child: buildCustomButton(context, "Share", () {})),
                  ],
                ),
                SizedBox(height: 20),
                RecentChecks(),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
