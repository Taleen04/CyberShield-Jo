import 'package:cyper_shield_jo/core/constants/app_colors.dart';
import 'package:cyper_shield_jo/core/utils/reponsive_size_helper.dart';
import 'package:cyper_shield_jo/feature/home_feature/presentation/views/widgets/perc_circle.dart';
import 'package:flutter/material.dart';

class BuildBoxResult extends StatelessWidget {
  const BuildBoxResult({super.key});

  final percOfRisk = 80;

  Widget getRiskLevel(BuildContext context) {
    if (percOfRisk > 70) {
      return resultBox(
        context,
        "High Risk detected",
        "Scam",
        AppColors.redColor,
        "This link is a scam",
        AppColors.redColor.withOpacity(0.1),
      );
    } else if (percOfRisk > 40) {
      return resultBox(
        context,
        "Medium Risk detected",
        "Phishing",
        AppColors.orangeColor,
        "This link is a phishing",
        AppColors.orangeColor.withOpacity(0.1),
      );
    } else {
      return resultBox(
        context,
        "Low Risk detected",
        "Appears safe",
        AppColors.greenColor,
        "This link is safe",
        AppColors.greenColor.withOpacity(0.1),
      );
    }
  }

  Widget resultBox(
    BuildContext context,
    String resultText,
    String alertText,
    Color color,
    String message,
    Color backgroundColor,
  ) {
    final screenWidth = MediaQuery.of(context).size.width;

    double maxWidth = screenWidth < 800 ? screenWidth : 600;

    return Padding(
      padding: EdgeInsets.symmetric(horizontal: screenWidth < 600 ? 16 : 40),
      child: Center(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: maxWidth),
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: backgroundColor,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: AppColors.surfaceColor.withOpacity(0.08),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    PercentageCircle(percentage: 0.8),

                    SizedBox(width: responsiveWidth(context, 16)),

                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            resultText,
                            style: TextStyle(
                              color: AppColors.whiteColor,
                              fontSize: screenWidth < 600 ? 16 : 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),

                          SizedBox(height: responsiveHeight(context, 10)),

                          Wrap(
                            spacing: 10,
                            runSpacing: 8,
                            children: [
                              Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 4,
                                ),
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(16),
                                  color: color.withOpacity(0.2),
                                ),
                                child: Text(
                                  alertText,
                                  style: TextStyle(color: color),
                                ),
                              ),
                            ],
                          ),

                          SizedBox(height: responsiveHeight(context, 10)),

                          Text(
                            message,
                            style: TextStyle(
                              color: AppColors.whiteColor.withOpacity(0.7),
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),

                SizedBox(height: responsiveHeight(context, 20)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return getRiskLevel(context);
  }
}
