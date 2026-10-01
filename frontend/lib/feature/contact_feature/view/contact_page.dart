import 'package:flutter/material.dart';
import 'package:cyper_shield_jo/core/constants/app_colors.dart';

class ContactPage extends StatelessWidget {
  const ContactPage({super.key});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;

    double titleSize = width < 600 ? 22 : 28;

    return Scaffold(
      backgroundColor: AppColors.backgroundColor,

      appBar: AppBar(
        backgroundColor: AppColors.backgroundColor,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "Contact Us",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 10),

            Text(
              "We’re here to help you stay safe online",
              textAlign: TextAlign.center,
              style: TextStyle(
                color: AppColors.grayColor,
                fontSize: width < 600 ? 14 : 16,
              ),
            ),

            const SizedBox(height: 20),

            _buildCard(
              icon: Icons.email,
              title: "Email Support",
              value: "support@cybershield.com",
              color: Colors.blue,
            ),

            _buildCard(
              icon: Icons.location_on,
              title: "Location",
              value: "Amman, Jordan",
              color: Colors.blue,
            ),

            _buildCard(
              icon: Icons.phone,
              title: "Phone Support",
              value: "+962 7XX XXX XXX",
              color: Colors.green,
            ),

            _buildCard(
              icon: Icons.chat,
              title: "Live Chat",
              value: "Available 24/7 inside the app",
              color: Colors.purple,
            ),

            _buildCard(
              icon: Icons.report_problem,
              title: "Report a Scam",
              value: "Use the Add Report button in the app",
              color: Colors.red,
            ),

            const Spacer(),
          ],
        ),
      ),
    );
  }

  Widget _buildCard({
    required IconData icon,
    required String title,
    required String value,
    required Color color,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.surfaceColor,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          Container(
            width: 45,
            height: 45,
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: color),
          ),

          const SizedBox(width: 12),

          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: TextStyle(color: AppColors.grayColor, fontSize: 13),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
