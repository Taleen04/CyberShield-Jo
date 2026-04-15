import 'package:flutter/material.dart';
import 'package:cyper_shield_jo/core/constants/app_colors.dart';

class CyberAwarenessPage extends StatelessWidget {
  const CyberAwarenessPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundColor,

      appBar: AppBar(
        backgroundColor: AppColors.backgroundColor,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "Cyber Awareness",
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),

      body: ListView(
        padding: const EdgeInsets.only(bottom: 20),
        children: [
          _buildCard(
            context,
            icon: Icons.link,
            color: Colors.red,
            title: "Phishing Links (Most Common)",
            desc:
                "Fake links that look like banks, social media or government sites used to steal passwords.",
          ),

          _buildCard(
            context,
            icon: Icons.qr_code,
            color: Colors.orange,
            title: "QR Code Scams",
            desc:
                "Hackers replace QR codes in public places or emails to redirect you to fake websites.",
          ),

          _buildCard(
            context,
            icon: Icons.sms,
            color: Colors.blue,
            title: "Fake SMS & WhatsApp Messages",
            desc:
                "Messages claiming 'your account is locked' or 'verify now' to trick you into clicking malicious links.",
          ),

          _buildCard(
            context,
            icon: Icons.lock,
            color: Colors.purple,
            title: "OTP & Verification Theft",
            desc:
                "Never share OTP codes. Scammers use them to access your bank or social accounts instantly.",
          ),

          _buildCard(
            context,
            icon: Icons.work,
            color: Colors.green,
            title: "Fake Job Offers",
            desc:
                "Scam recruiters ask for fees or personal documents under fake job opportunities.",
          ),

          _buildCard(
            context,
            icon: Icons.currency_bitcoin,
            color: Colors.amber,
            title: "Crypto Investment Scams",
            desc:
                "Fake investment platforms promise high returns and disappear with your money.",
          ),

          _buildCard(
            context,
            icon: Icons.account_balance,
            color: Colors.redAccent,
            title: "Bank Impersonation",
            desc:
                "Scammers pretend to be your bank asking for account details or passwords.",
          ),

          _buildCard(
            context,
            icon: Icons.face,
            color: Colors.deepPurple,
            title: "AI Deepfake Scams",
            desc:
                "Fake voice or video calls pretending to be someone you trust to steal money or info.",
          ),

          _buildCard(
            context,
            icon: Icons.local_shipping,
            color: Colors.teal,
            title: "Fake Delivery Messages",
            desc:
                "Messages claiming you have a package waiting and asking for payment or details.",
          ),

          _buildCard(
            context,
            icon: Icons.public,
            color: Colors.cyan,
            title: "Public Wi-Fi Attacks",
            desc:
                "Hackers can intercept your data when using unsecured public networks.",
          ),
        ],
      ),
    );
  }

  Widget _buildCard(
    BuildContext context, {
    required IconData icon,
    required Color color,
    required String title,
    required String desc,
  }) {
    final width = MediaQuery.of(context).size.width;

    return Container(
      margin: const EdgeInsets.only(bottom: 12, left: 16, right: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.surfaceColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.25)),
      ),
      child: Row(
        children: [
          Container(
            width: 46,
            height: 46,
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
                  style: TextStyle(
                    color: AppColors.whiteColor,
                    fontSize: width < 600 ? 15 : 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  desc,
                  style: TextStyle(
                    color: AppColors.grayColor,
                    fontSize: width < 600 ? 12 : 14,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
