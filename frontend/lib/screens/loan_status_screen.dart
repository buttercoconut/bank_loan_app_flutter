import 'package:flutter/material.dart';
import '../services/loan_api_service.dart';

class LoanStatusScreen extends StatefulWidget {
  final String loanId;
  const LoanStatusScreen({Key? key, required this.loanId}) : super(key: key);

  @override
  State<LoanStatusScreen> createState() => _LoanStatusScreenState();
}

class _LoanStatusScreenState extends State<LoanStatusScreen> {
  late Future<Map> _loanFuture;

  @override
  void initState() {
    super.initState();
    _loanFuture = LoanApiService.getLoan(widget.loanId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('대출 상태')),
      body: FutureBuilder<Map>(
        future: _loanFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Text(
                '오류: ${snapshot.error}',
                style: const TextStyle(color: Colors.red),
              ),
            );
          }
          if (!snapshot.hasData) {
            return const Center(child: Text('대출 정보를 찾을 수 없습니다.'));
          }
          final data = snapshot.data!;
          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('대출 ID: ${widget.loanId}', style: const TextStyle(fontSize: 18)),
                const SizedBox(height: 10),
                Text('금액: ${data['amount']}', style: const TextStyle(fontSize: 16)),
                Text('기간: ${data['term_months']}개월', style: const TextStyle(fontSize: 16)),
                Text('상태: ${data['status']}', style: const TextStyle(fontSize: 16)),
              ],
            ),
          );
        },
      ),
    );
  }
}
