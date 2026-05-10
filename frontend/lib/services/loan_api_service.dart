import 'dart:convert';
import 'package:http/http.dart' as http;

class LoanApiService {
  static const _baseUrl = 'https://api.example.com/loans';

  static Future<String> applyLoan({required double amount, required int termMonths}) async {
    final response = await http.post(
      Uri.parse(_baseUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'amount': amount, 'term_months': termMonths}),
    );
    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return data['loan_id'];
    } else {
      throw Exception('대출 신청 실패: ${response.statusCode}');
    }
  }

  static Future<Map<String, dynamic>> getLoan(String loanId) async {
    final response = await http.get(Uri.parse('$_baseUrl/$loanId'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      throw Exception('대출 정보 조회 실패: ${response.statusCode}');
    }
  }
}
