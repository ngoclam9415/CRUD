Feature: Check synchronize between mysql and mongo

    Scenario Outline: Open website and create city
        Given Open city page
        When Create a new <city>
        Then Check if <city> is listed
        Then Check if <city> existed in mongo

        Examples:
        | city |
        | Hồ Chí Minh |
        | Hà Nội |
        | Hội An |
        | Đà Nẵng |
        | Quy Nhơn |
        | Đà Lạt |
        | Vĩnh Hy |
        | Quảng Nam |
        | Quảng Bình |
        | Quảng Ngãi |
        | Nha Trang |
        | Hạ Long |
        | Sapa |

    Scenario Outline: Open website and search city
        Given Previous create step
        When Search with <keyword>
        Then Check if <city> listed in search results

        Examples:
        | keyword | city |
        | Chi | Hồ Chí Minh |
        | Minh | Hồ Chí Minh |
        | Hồ Chi | Hồ Chí Minh |
        | Ha | Hà Nội |
        | Nội | Hà Nội |
        | Hồ Chí Minh | Hồ Chí Minh |
        | Hà Nội | Hà Nội |
        | Hội An | Hội An |
        | Đà Nẵng | Đà Nẵng |
        | Quy | Quy Nhơn |
        | Lạt | Đà Lạt |
        | Hy | Vĩnh Hy |
        | Nam | Quảng Nam |
        | Quảng Bonh | Quảng Bình |
        | Quảng Ngii | Quảng Ngãi |
        | Nga Trang | Nha Trang |
        | Hạ Leng | Hạ Long |
        | Sapa | Sapa |