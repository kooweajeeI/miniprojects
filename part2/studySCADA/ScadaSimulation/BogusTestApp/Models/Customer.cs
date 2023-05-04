using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTestApp.Models
{
    public class Customer // 고객 테이블과 매핑
    {
        public Guid Id { get; set; }                    // 고객 아이디
        public string Name { get; set; }                // 고객 명
        public string Address { get; set; }             // 고객 주소
        public string Phone { get; set; }               // 고객 전화번호
        public string ContactName { get; set; }         // 고객 연락처 명
        public IEnumerable<Order> Orders { get; set; }  // 고객이 주문한 리스트
    }
}
