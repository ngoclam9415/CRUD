Feature: Check synchronize between mysql and mongo

    Scenario Outline: Open website and create city
        Given Open city page
        When Create a new <city>
        Then Check if <city> is listed
        Then Check if <city> existed in mongo

        Examples:
        | city |
        | Ho Chí Minh |
        | Hà Noi |
        | Hoi An |
        | Dà Nang |
        | Quy Nhơn |
        | Da Lat |
        | Vĩnh Hy |
        | Quảng Nam |
        | Quảng Bình |
        | Quảng Ngãi |
        | Nha Trang |
        | Ha Long |
        | Sapa |

    Scenario Outline: Open website and search city
        Given Previous create step
        When Search with <keyword>
        Then Check if <city> listed in search results

        Examples:
        | keyword | city |
        | Chi | Ho Chí Minh |
        | Minh | Ho Chí Minh |
        | Ho Chi | Ho Chí Minh |
        | Ha | Hà Noi |
        | Noi | Hà Noi |
        | Ho Chí Minh | Ho Chí Minh |
        | Hà Noi | Hà Noi |
        | Hoi An | Hoi An |
        | Dà Nang | Dà Nang |
        | Quy | Quy Nhơn |
        | Lat | Da Lat |
        | Hy | Vĩnh Hy |
        | Nam | Quảng Nam |
        | Quảng Bonh | Quảng Bình |
        | Quảng Ngii | Quảng Ngãi |
        | Nga Trang | Nha Trang |
        | Ha Leng | Ha Long |
        | Sapa | Sapa |

    Scenario Outline: Open website and edit city
        Given Open city page
        When Edit <city> with <new_city>
        Then Check if <new_city> is listed in current page
        Then Check if <new_city> existed in mongo

        Examples:
        | city | new_city |
        | Ho Chí Minh | Minh Chí Ho |
        | Hà Noi | Noi Hà |
        | Hoi An | Hoi Angggg |
        | Dà Nang | Dà Nẽng |
        | Quy Nhơn | Phung Quy |
        | Quảng Nam | Nam Quảng |
        | Quảng Bình | Bình Quảng |
        | Quảng Ngãi | Ngãi Quảng |

    Scenario Outline: Open website and search city
        Given Previous create step
        When Search with <keyword>
        Then Check if <city> listed in search results

        Examples:
        | keyword | city |
        | Chi | Minh Chí Ho |
        | Minh | Minh Chí Ho |
        | Ho Chi | Minh Chí Ho |
        | Ha | Noi Hà |
        | Noi | Noi Hà |
        | Minh Chí Ho | Minh Chí Ho |
        | Noi Hà | Noi Hà |
        | Hoi An | Hoi Angggg |
        | Dà Nang | Dà Nẽng |
        | Quy | Phung Quy |
        | Lat | Da Lat |
        | Hy | Vĩnh Hy |
        | Nam | Nam Quảng |
        | Quảng Bonh | Bình Quảng |
        | Quảng Ngii | Ngãi Quảng |
        | Nga Trang | Nha Trang |
        | Ha Leng | Ha Long |
        | Sapa | Sapa |