GROUP = [
    (0, "Customer"),
    (1, "Merchant"),
    (2, "Employee"),
    (3, "Manager"),
    (4, "SysAdmin"),
]
# (5, "Approved") is a group but not one of the choices available during sign up, so not part of above
# But is part of below maps


MAP = {0: "Customer",
       1: "Merchant",
       2: "Employee",
       3: "Manager",
       4: "SysAdmin",
       5: "Approved",
       }

R_MAP = {"Customer": 0,
         "Merchant": 1,
         "Employee": 2,
         "Manager": 3,
         "SysAdmin": 4,
         "Approved": 5,
         }
