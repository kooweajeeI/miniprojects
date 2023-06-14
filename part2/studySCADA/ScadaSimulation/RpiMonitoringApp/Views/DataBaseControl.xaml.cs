using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using Org.BouncyCastle.Bcpg.OpenPgp;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>


    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; }

        Thread MqttThread { get; set; }     // 없으면 UI컨트롤이 어려워짐

        int MaxCount { get; set; } = 10;

        // MQTT Subscribition text 과도문제 속도저하를 잡기위해 변수

        public DataBaseControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false;
            BtnConnDb.IsChecked = false;

            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                IsConnected = true;
                BtnConnDb.Content = "MQTT 연결중";
                BtnConnDb.IsChecked = true;
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
        }

        // 토글버튼 클릭 (1: 접속 2: 접속끊기) 이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            ConnectDB();            
        }

        private void ConnectDB()
        {
            if (IsConnected == false)
            {

                // MQTT 브로커에 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    // MQTT 구독 로직처리
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {

                        // MQTT 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR"); // clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                                new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE }); // QOS는 네트워크 통신 옵션
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDb.IsChecked = true;
                        IsConnected = true;

                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 : {ex.Message}");
                }
            }
            else
            {
                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateLog(">>> MQTT Broker Disconnrcted...");

                        BtnConnDb.IsChecked = false;
                        IsConnected = false;
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 : {ex.Message}");
                }
            }
        }

        private void UpdateLog(string msg)
        {
            // 예외처리 필요
            this.Invoke(() => {
                if (MaxCount <= 0)
                {
                    TxtLog.Text = string.Empty;
                    TxtLog.Text += ">>>문서 건수가 많아져 초기화!\n";
                    TxtLog.ScrollToEnd();
                    MaxCount = 10;
                }
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
                MaxCount--;
            });
        }

        // 구독이 발생할떄마다 실행되는 이벤트
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic);    // 실제 DB에 저장
        }

        // DB저장처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null)
            {
                Debug.WriteLine(currValue["DEV_ID"]);
                Debug.WriteLine(currValue["TYPE"]);
                Debug.WriteLine(currValue["CURR_DT"]);
                Debug.WriteLine(currValue["STAT"]);

                var tmp = currValue["STAT"].Split('|');
                var temp = tmp[0].Trim();
                var humid = tmp[1].Trim();

                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = @"INSERT INTO smarthomesensor
                                            (Home_Id,
                                            Room_Name,
                                            Sensing_DateTime,
                                            Temp,
                                            Humid)
                                            VALUES
                                            (@Home_Id,
                                            @Room_Name,
                                            @Sensing_DateTime,
                                            @Temp,
                                            @Humid)";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["DEV_ID"]);
                        cmd.Parameters.AddWithValue("@Room_Name", currValue["TYPE"]);
                        cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["CURR_DT"]);
                        cmd.Parameters.AddWithValue("@Temp", temp);
                        cmd.Parameters.AddWithValue("@Humid", humid);

                        if (cmd.ExecuteNonQuery() == 1)
                        {
                            UpdateLog(">>> DB Insert 성공");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert 실패");
                        }
                    }
                }
                catch (Exception ex)
                {

                    UpdateLog($"!!! Error 발생 : {ex.Message}");
                }
            }
        }
    }
}