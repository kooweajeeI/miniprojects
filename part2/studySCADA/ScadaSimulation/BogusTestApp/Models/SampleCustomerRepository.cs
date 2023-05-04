using Bogus;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTestApp.Models
{
    public class SampleCustomerRepository
    {
        public IEnumerable<Customer> GetCustomers(int genNum)
        {
            /*
            var list = new List<Customer>();
            list.Add(new Customer
            {
                Id = Guid.NewGuid(),
                Name = "홍길동",
                Address = "부산"
            });
            list.Add(new Customer
            {
                Id = Guid.NewGuid(),
                Name = "홍길순",
                Address = "대구"
            });
            */
            // Randomizer -> Bogus로 Random과 다름
            Randomizer.Seed = new Random(123456); // Seed 수 결정 Random(숫자 마음대로 결정)
            
            // 아래와 같은 규칙으로 주문 더미데이터 생성
            var orderGen = new Faker<Order>()
                .RuleFor(o => o.Id, Guid.NewGuid) // ID값은 GUI로 자동 생성
                .RuleFor(d => d.Date, f => f.Date.Past(3)) // 날짜를 3년 전으로 세팅
                .RuleFor(o => o.OrderValue, f => f.Finance.Amount(1, 10000)) // 1부터 10000숫자 중 랜덤
                .RuleFor(o => o.Shipped, f => f.Random.Bool(0.8f)); // 80% = true / 0.5f -> true/false 반반

            // 고객 더미 데이터 생성 규칙
            var customerGen = new Faker<Customer>()
                .RuleFor(c => c.Id, Guid.NewGuid())
                .RuleFor(c => c.Name, f => f.Company.CompanyName())
                .RuleFor(c => c.Address, f => f.Address.FullAddress())
                .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber())
                .RuleFor(c => c.ContactName, f => f.Name.FullName())
                .RuleFor(c => c.Orders, f => orderGen.Generate(f.Random.Number(1, 2)).ToList());

            return customerGen.Generate(genNum); // 10개의 가짜 고객 데이터 생성, 리턴
        }
    }
}
