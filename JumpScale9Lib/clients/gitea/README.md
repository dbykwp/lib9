**Get Gitea Client**
```

In [1]: cl = j.clients.gitea.get()
In [2]: cl
Out[2]: <Gitea Client: v=1.1.0+898-ge2e692ce user=hamdy admin=True>
```

**Get Gitea Client version**
```
In [3]: cl.version
Out[3]: '1.1.0+898-ge2e692ce'
```

**Markdown Manager**
```
In [4]: cl.markdowns
Out[4]: <Gitea MarkDown Manager>
In [5]: cl.markdowns.render(text="##This is header")
Out[5]: b'<h2>This is header</h2>\n'

In [8]: cl.markdowns.render_raw(text="##This is header")
Out[8]: b'<p>{&quot;body&quot;: &quot;##This is header&quot;}</p>\n'

```

### Users Manager

**Current user**
```
In [2]: cl.users.current
Out[2]:

<Current User>
{
    "id": 1,
    "username": "hamdy",
    "email": "hamdy@greenitglobe.com",
    "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"
}

# Client automatically detects that `hamdy` is current user

In [3]: cl.users.get(username='hamdy')
Out[3]:

<Current User>
{
    "id": 1,
    "username": "hamdy",
    "email": "hamdy@greenitglobe.com",
    "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"
}


In [2]: cl.users.current.is_admin
Out[2]: True

In [3]: cl.users.current.follow('ooo')
Out[3]: True

In [4]: cl.users.current.is_following('ooo')
Out[4]: True

In [5]: cl.users.current.unfollow('ooo')
Out[5]: True

In [6]: cl.users.current.is_following('oooooo')
Out[6]: False


In [4]: cl.users.current.follow('oooooooo')
[Wed23 15:11] - GiteaUserCurrent.py:21  :j.giteausercurrent   - DEBUG    - username does not exist
Out[4]: False

In [5]: cl.users.current.unfollow('oooooooo')
[Wed23 15:11] - GiteaUserCurrent.py:30  :j.giteausercurrent   - DEBUG    - username does not exist
Out[5]: False

In [2]: cl.users.current.emails
Out[2]: <Gitea Emails Iterator for user: hamdy>

In [3]: [e for e in cl.users.current.emails]
Out[3]:
[
 <Gitea Email>
 {
     "email": "hamdy@greenitglobe.com",
     "verified": true,
     "primary": true
 }]

In [4]: cl.users.current.emails.add(emails=['ham@e.com'])
Out[4]: True

In [5]: cl.users.current.emails.add(emails=['ham@e.com'])
[Wed23 20:59] - GiteaUserCurrentEmails.py:21  :giteausercurrentemails - DEBUG    - b'{"message":"Email address has been used: ham@e.com","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}'
Out[5]: False

In [6]: cl.users.current.emails.remove(emails=['ham@e.com'])
Out[6]: True

In [7]:

In [7]: cl.users.current.emails.remove(emails=['ham@e.com'])
[Wed23 20:59] - GiteaUserCurrentEmails.py:29  :giteausercurrentemails - DEBUG    - b'{"message":"Email address does not exist","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}'
Out[7]: False

```

**Search**

```
In [4]: cl.users
Out[4]: <Users>

In [2]: cl.users.is_following('hamdy', 'oooo')
[Wed23 21:16] - GiteaUsers.py     :66  :j.giteausers         - DEBUG    - follower or followee not found
Out[2]: False

In [3]: cl.users.is_following('hamdy', 'ooo')
Out[3]: True

In [2]: cl.users.search(query='ham')
Out[2]:
[
 <Current User>
 {
     "id": 1,
     "username": "hamdy",
     "email": "hamdy@greenitglobe.com",
     "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"
 },
 <User>
 {
     "id": 90,
     "username": "hamdy2",
     "email": "jh@we.com",
     "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon"
 }]

In [3]: cl.users.search(query='ham', limit=1)
Out[3]:
[
 <Current User>
 {
     "id": 1,
     "username": "hamdy",
     "email": "hamdy@greenitglobe.com",
     "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"
 }]

```

**Get a user by username**

```
In [5]: cl.users.get(username='hamdy2')
Out[5]:

<User>
{
    "id": 90,
    "username": "hamdy2",
    "email": "jh@we.com",
    "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon"
}
```

**Admin Operations**

`If current user is not admin, these operations will fail`

```
In [2]: user = cl.users.new()
In [3]: user.save()

[Wed23 22:22] - GiteaUser.py      :152 :j.giteauser          - DEBUG    - create Error {"password": "Missing", "username": "Missing", "email": "Missing"}
Out[3]: False

In [4]: user.username = 'hamdy'

In [5]: user.password = '123456'

In [6]: user.email = 's@w.com'

In [7]: user.save()
[Wed23 22:23] - GiteaUser.py      :162 :j.giteauser          - DEBUG    - b'{"message":"user already exists [name: hamdy]","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}'
Out[7]: False

In [8]: user.username = 'hamdy11'

In [9]: user.save()
Out[9]: True

In [10]: user.save()
[Wed23 22:23] - GiteaUser.py      :152 :j.giteauser          - DEBUG    - create Error {"id": "Already existing"}
Out[10]: False

In [11]: user.email = 'oto@er.com'
In [12]: user.update()
Out[12]: True

In [13]: user.delete()
Out[13]: True

In [14]: user.save()
Out[14]: True
```

**Keys management**
```
In [2]: cl.users.current.keys
Out[2]: <PublicKeys Iterator for user: hamdy>

In [4]: [k for k in cl.users.current.keys]
Out[4]: []

In [5]: k = cl.users.current.keys.new()

In [6]: k.title = 'helllo key'

In [7]: k.key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4IN8ZGDgdgDeul8h49yResQBfVI1wIFsleD+O8Y3YTdYw97A9MgFZJcNGM
   ...: OOs1vGXYlyzVT6+gCFADHyzpSCYjs82qn6UljjUNes0OyxmCnE1wuPCPIV7IuUkr9Zt+Ca3+hOAArQgs9X172mDj1vojLYg/ttBCNCvv1Y
   ...: H+khZSmSxdhgFICrUa2ROP98REwPG9vMl5KQzUnO8xnBUYHucLGPYn9stECM81SQRTOK6hZPhok/38ymecL8NtFws47MeqkeD4k4tvB69L
   ...: GYc3A1iXbnyghFp6tqjQ5s2H7EWkBU4v2jNnCQALWGJX5mJpvEXMxkGbJgM8gUnCEKVCkP1"

In [8]: k.save()
Out[8]: True

In [12]: k.delete()
Out[12]: True

In [13]: [k for k in cl.users.current.keys]
Out[13]: []

# Create a pub key for user / requires admin

In [8]: k = cl.users.get(username='ooo', fetch=False).keys.new()

In [9]: k.title= 'ss'

In [10]: k.key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4IN8ZGDgdgDeul8h49yResQBfVI1wIFsleD+O8Y3YTdYw97A9MgFZJcNG
    ...: MOOs1vGXYlyzVT6+gCFADHyzpSCYjs82qn6UljjUNes0OyxmCnE1wuPCPIV7IuUkr9Zt+Ca3+hOAArQgs9X172mDj1vojLYg/ttBCNCvv
    ...: 1YH+khZSmSxdhgFICrUa2ROP98REwPG9vMl5KQzUnO8xnBUYHucLGPYn9stECM81SQRTOK6hZPhok/38ymecL8NtFws47MeqkeD4k4tvB
    ...: 69LGYc3A1iXbnyghFp6tqjQ5s2H7EWkBU4v2jNnCQALWGJX5mJpvEXMxkGbJgM8gUnCEKVCkP1"

In [11]: k.save()
Out[11]: True

In [12]: k.id
Out[12]: 19

In [8]: cl.users.current.keys.get(20)
Out[8]:

<Public Key: user=hamdy>
{
    "id": 20,
    "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4xOQsSroXRH/34ET7VOHqqxb0oWTYR1fXlXeaY6kTt4U5n7N2YWKhhavZNIzc8aBznch+0YDSby/Xf0Ld8omFOIueKim6vwcrMDqKKqH/iduDQckbzmaPwMbuZyEDQLUsB3zMmBPvhWe2W92jD4jk3Fes/DrhTVdr59f9hzvYNI+pNk7IrM1QukLJN9xumitfvr2aTl6MRfFyG65uDLgV3dqVSVj1m1pTUpjSYqSltI8GVoD8SNwzbamSyVkHnYKyzTs8XdsCh655R4d56BQZQnSm1d98veLHdh9TLsaCnrkNB8qkYFYucuMQRQFvmkrUcin0BDBTLpyZPybdzKC9 root@js",
    "title": "er",
    "created_at": "2018-05-24T12:01:26Z",
    "fingerprint": "SHA256:IJW59oGBQ/xk9oCsHtuRtJ9z9fQOwQUg0/GSGIy9jCs",
    "url": "http://172.17.0.2:3000/api/v1/user/keys/20"
}


# GPG keys
In [2]: cl.users.current.gpg_keys
Out[2]: <GpgKeys Iterator for user: hamdy>

In [2]: k = cl.users.current.gpg_keys.new()

In [3]: P8mtlwubRhgKCDB4GdJFJPpvkAB56HZMBb1s05w3xSswPAurZNPv3jxEzS7u7mfh
   ...: d/FTSXe79TnqRmNkv6TWZnsdV7Qq2fme3/WFCko81GWruRxD2hjcpFTH/tli/F/i
   ...: olnNme6zkhb+0xnH4XIkS51g479nRF+txhBx/RZ0jQwPy59CofWQADKUORReFHh3
   ...: jUWoyK7x3QARAQABtB5IYW1keSA8aGFtZHlAZ3JlZW5pdGdsb2JlLmNvbT6JATcE
   ...: EwEIACEFAlsGpDkCGwMFCwkIBwIGFQgJCgsCBBYCAwECHgECF4AACgkQGVv9wmI/
   ...: H9rnWwf9EQq39qeBre3W9tlA2fIzIxTmLaTTTKexBRHP92nIjQi30IfSqREkRgru
   ...: V4H+kA2yQp2tkC51nsn4a4L7UNrWqONa7+JfwN7b1HRSHAkVnvorKvYyGo4HFK46
   ...: jqcBTMfjXnBvB7k1TRE5ziJ16zOxuW5IQ2+9R4H2L4s4aZqkG+L3nNC1COInN5r5
   ...: YRDGKdkesTQAu43CjGFhLJj+kO8zbq6QxYBmZ8VEpYDUgPTqgjsK+ufacAsyg6km
   ...: VMwAQb8dsE982WUGUvP8vTqydvCeLMeaHrPc/D1BzSwglltHBgExTFh46viSjZdz
   ...: /PN8mg3i+BIMoVYbKadECssYvmkjM7kBDQRbBqQ5AQgAqwZE36xHUx5qp2z1xAOX
   ...: APz1eGfjzWvppVrKWypSPJjToOoWhzKYiB+6F1LWis38kePPE2M1Beh0jjVBazXO
   ...: LBseJTwBCaZFz461XPFs46k7jW+tUnDpWDXCHj6sQJ16MEsAlNiK3FHn6VBVjq1e
   ...: Nd9rEO4NlfyabIHOmjoCxEPWYvO3XG9x73Kxl3pIM23T4PeA9in8RldY7YJOSeav
   ...: viJ3Vnzvr3Ff0gkMRtLbkYO97qKqzwpXc8SXin697Du8wWBfIhzJuBOYdk+HLIQH
   ...: GEGGRQs/fVg9cytiRRxlwXFOwFSkVO3Rdi9MVbrx2/Z5CiRFqG73CmmDW/+qhuWQ
   ...: xQARAQABiQEfBBgBCAAJBQJbBqQ5AhsMAAoJEBlb/cJiPx/a9osIAKO4TUrdcyMf
   ...: ltBA7TTbzvd+xFGc/lk/Py+ArTsT3MaQBXkAY/dmAlur8I8ZHowvuL/EF5CCf9OL
   ...: sAU3MYbjVTPs8d57QOdMKu/w7RviQBuBiDZDWZcx45bQC6jh3Ybhz9piYkjjapRM
   ...: N9syB55pTgJPEJTIx6jB+9mXBplxVUFmUYBGjhd9yE54P+qhtL0zMjRcen1sIm2Z
   ...: QtmLX59IAcbm8uV/3P1ZmvCU2vuEsxrkUcQ45hIQOQVyLLpBggdxBD6rBF0ge7fX
   ...: mP5WVsiap4cwNKQ/hK80IdZ36NJrOHkCYZ2g6oyr7jHqxaWUq3vFH4Q+YCptCKq+
   ...: CusbC/Kr6Hk=
   ...: =Qwfp
   ...: -----END PGP PUBLIC KEY BLOCK-----
   ...: """

In [4]: k.save()
Out[4]: True

In [5]: [g for g in cl.users.current.gpg_keys]
Out[5]:
[
 <GPG Key: user=hamdy>
 {
     "id": 3,
     "can_encrypt_comms": true,
     "can_certify": true,
     "created_at": "2018-05-09T11:51:10Z",
     "can_sign": true,
     "emails": [
         {
             "email": "hamdy@greenitglobe.com",
             "verified": true
         }
     ],
     "expires_at": "0001-01-01T00:00:00Z",
     "key_id": "EA7651D0187EC25A",
     "can_encrypt_storage": true,
     "primary_key_id": "                ",
     "public_key": "xsBNBFry4K4BCAC9L/ULGqYxmC6Zuk2akcVWun1KnMo5vKiDJXthgUGruq6lA6pgMzEi0xKF0dtHGRZcB3xvu2CMhbtMddbE9S40kUoYkXUnuybyNF/lQGf+L92/oY7Cs6QumvaFVIpudQ/A1t9PDeasWa4TwxMYmpdOiJbXR52qXcE6IEuOxsCriJFOLzHXHg+ef0DjlsD85WeDz0Jmr8lr719e3zFgqGPbUX1SiDMlAZOPLef2jiqPHRUvNK/DOTSJi/76jB0bH77JKtgUClNEPg8rgAhhq+yQEbDI8iPEGFFEuxvdRZBX5B+pLCKK6SiJ+OMskkjxu12Tzwdi61yRD9B9xx9cvyqPABEBAAE=",
     "subkeys": [
         {
             "id": 4,
             "primary_key_id": "EA7651D0187EC25A",
             "key_id": "E5C39437A273FF70",
             "public_key": "zsBNBFry4K4BCADLV4XZ2golau1KGwPSeoz1onamxkUcijs0Cgi11mcQgYi94Llnehxj4U+OAzsp+pCz/3LUZfgjBNG0/CDu/0q2tHXqvE9On8VZAXgPFKhwmuieR6bpEDT4IX/9D+M4Ic9T2Gx+2Pyd+pJo/0qzEHpR1pW/66faEcePhr/asfh3tMJy5riuQu5c2hHErkmRkLYKGITsGlJkE8kqha11zUZlYoSWPPwc38m/7FcZC4jLnBSE4h11tJ17x7s1HNwCe9tn8lU4wvcw7tUz7sGe/dFO+euW8HFm3kCHRVsWOgkI/zQgAV3u45exjwEiYr1aOeT0H/yhpLW4jPHAIZiKR+fnABEBAAE=",
             "emails": null,
             "subkeys": null,
             "can_sign": true,
             "can_encrypt_comms": true,
             "can_encrypt_storage": true,
             "can_certify": true,
             "created_at": "2018-05-09T11:51:10Z",
             "expires_at": "0001-01-01T00:00:00Z"
         }
     ]
 }]

In [6]: k.delete()
Out[6]: True

In [7]: [g for g in cl.users.current.gpg_keys]
Out[7]: []

In [16]: cl.users.current.gpg_keys.get(5)
Out[16]:

<GPG Key: user=hamdy>
{
    "id": 5,
    "can_encrypt_comms": true,
    "can_certify": true,
    "created_at": "2018-05-09T11:51:10Z",
    "can_sign": true,
    "emails": [
        {
            "email": "hamdy@greenitglobe.com",
            "verified": true
        }
    ],
    "expires_at": "0001-01-01T00:00:00Z",
    "key_id": "EA7651D0187EC25A",
    "can_encrypt_storage": true,
    "primary_key_id": "                ",
    "public_key": "xsBNBFry4K4BCAC9L/ULGqYxmC6Zuk2akcVWun1KnMo5vKiDJXthgUGruq6lA6pgMzEi0xKF0dtHGRZcB3xvu2CMhbtMddbE9S40kUoYkXUnuybyNF/lQGf+L92/oY7Cs6QumvaFVIpudQ/A1t9PDeasWa4TwxMYmpdOiJbXR52qXcE6IEuOxsCriJFOLzHXHg+ef0DjlsD85WeDz0Jmr8lr719e3zFgqGPbUX1SiDMlAZOPLef2jiqPHRUvNK/DOTSJi/76jB0bH77JKtgUClNEPg8rgAhhq+yQEbDI8iPEGFFEuxvdRZBX5B+pLCKK6SiJ+OMskkjxu12Tzwdi61yRD9B9xx9cvyqPABEBAAE=",
    "subkeys": [
        {
            "id": 6,
            "primary_key_id": "EA7651D0187EC25A",
            "key_id": "E5C39437A273FF70",
            "public_key": "zsBNBFry4K4BCADLV4XZ2golau1KGwPSeoz1onamxkUcijs0Cgi11mcQgYi94Llnehxj4U+OAzsp+pCz/3LUZfgjBNG0/CDu/0q2tHXqvE9On8VZAXgPFKhwmuieR6bpEDT4IX/9D+M4Ic9T2Gx+2Pyd+pJo/0qzEHpR1pW/66faEcePhr/asfh3tMJy5riuQu5c2hHErkmRkLYKGITsGlJkE8kqha11zUZlYoSWPPwc38m/7FcZC4jLnBSE4h11tJ17x7s1HNwCe9tn8lU4wvcw7tUz7sGe/dFO+euW8HFm3kCHRVsWOgkI/zQgAV3u45exjwEiYr1aOeT0H/yhpLW4jPHAIZiKR+fnABEBAAE=",
            "emails": null,
            "subkeys": null,
            "can_sign": true,
            "can_encrypt_comms": true,
            "can_encrypt_storage": true,
            "can_certify": true,
            "created_at": "2018-05-09T11:51:10Z",
            "expires_at": "0001-01-01T00:00:00Z"
        }
    ]
}
```

**User Organizations**

```
In [2]: [o for o in cl.users.current.organizations]
Out[2]:
[
 <Organization>
 {
     "id": 87,
     "avatar_url": "http://172.17.0.2:3000/avatars/87",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "gigaya",
     "website": ""
 },
 <Organization>
 {
     "id": 89,
     "avatar_url": "http://172.17.0.2:3000/avatars/89",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "kk",
     "website": "http://hh.com"
 },
 <Organization>
 {
     "id": 88,
     "avatar_url": "http://172.17.0.2:3000/avatars/88",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "ss",
     "website": ""
 }]

In [2]: cl.users.get(username='ooo').is_member_of_org('koki')
[Thu24 13:21] - GiteaOrgs.py      :37  :j.giteaorgs          - DEBUG    - ooo is not member of organization koki
Out[2]: False

In [3]: cl.users.current.is_member_of_org('koki')
[Thu24 13:21] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koki
Out[3]: True
```

- Only members of an org, can update/try to delete
```
In [6]: org = cl.users.current.organizations.get('koki')
[Thu24 13:24] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koki


In [7]: org = cl.users.current.organizations.get('koki')
[Thu24 13:24] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koki

In [8]: org
Out[8]:

<Organization>
{
    "id": 95,
    "avatar_url": "http://172.17.0.2:3000/avatars/95",
    "description": "",
    "full_name": "",
    "location": "",
    "username": "koki",
    "website": ""
}

In [9]: org.description = "New desc"

In [10]: org.update()
Out[10]: True

In [11]: cl.users.current.organizations.get('koki')
[Thu24 13:24] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koki
Out[11]:

<Organization>
{
    "id": 95,
    "avatar_url": "http://172.17.0.2:3000/avatars/95",
    "description": "New desc",
    "full_name": "",
    "location": "",
    "username": "koki",
    "website": ""
}

In [12]: org = cl.users.get(username='ooo').organizations.get('koki')
[Thu24 13:25] - GiteaOrgs.py      :37  :j.giteaorgs          - DEBUG    - ooo is not member of organization koki

In [13]: org
Out[13]:

<Organization>
{
    "id": 95,
    "avatar_url": "http://172.17.0.2:3000/avatars/95",
    "description": "New desc",
    "full_name": "",
    "location": "",
    "username": "koki",
    "website": ""
}

In [14]: org.description = "yet another desc"

In [15]: org.update()
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
/usr/local/bin/js9 in <module>()
----> 1 org.update()

AttributeError: 'GiteaOrgForNonMember' object has no attribute 'update'
```

- Only admins can create organizations
```
In [3]: user = cl.users.get(username='ooo')

In [4]: org = user.organizations.new()

In [5]: org.username = 'one'

In [6]: org.save()
[Thu24 13:27] - GiteaOrgForMember.py:9   :j.giteaorgformember  - DEBUG    - create Error {"permissions": "Admin permissions required", "full_name": "Missing"}
Out[6]: False

In [7]: user = cl.users.current

In [8]: user.is_admin
Out[8]: True

In [9]: org = user.organizations.new()

In [10]: org.username = 'one'

In [11]: org.save()
[Thu24 13:28] - GiteaOrgForMember.py:9   :j.giteaorgformember  - DEBUG    - create Error {"full_name": "Missing"}
Out[11]: False

In [12]: org.full_name = 'One one'

In [13]: org.save()
Out[13]: True

In [14]: [org for org in cl.users.current.organizations]
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization gigaya
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization kk
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koki
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization koosa
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization one
[Thu24 13:29] - GiteaOrgs.py      :34  :j.giteaorgs          - DEBUG    - hamdy is member of organization ss
Out[14]:
[
 <Organization>
 {
     "id": 87,
     "avatar_url": "http://172.17.0.2:3000/avatars/87",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "gigaya",
     "website": ""
 },
 <Organization>
 {
     "id": 89,
     "avatar_url": "http://172.17.0.2:3000/avatars/89",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "kk",
     "website": "http://hh.com"
 },
 <Organization>
 {
     "id": 95,
     "avatar_url": "http://172.17.0.2:3000/avatars/95",
     "description": "New desc",
     "full_name": "",
     "location": "",
     "username": "koki",
     "website": ""
 },
 <Organization>
 {
     "id": 96,
     "avatar_url": "http://172.17.0.2:3000/avatars/96",
     "description": "",
     "full_name": "",
     "location": "",
     "username": "koosa",
     "website": ""
 },
 <Organization>
 {
     "id": 98,
     "avatar_url": "http://172.17.0.2:3000/avatars/98",
     "description": "",
     "full_name": "One one",
     "location": "",
     "username": "one",
     "website": ""
 },
 <Organization>
 {
     "id": 88,
     "avatar_url": "http://172.17.0.2:3000/avatars/88",
     "description": "ss",
     "full_name": "",
     "location": "",
     "username": "ss",
     "website": ""
 }]

```

### Repo Manager

```
In [8]: cl.repos
Out[8]: <General Repos finder and getter (by ID)>
```

**Search(name, mode, page_number=1, page_size=150, exclusive=False)**  *modes=("fork", "source", "mirror", "collaborative")*

```
        # search user repos
        repos = cl.users.get('hamdy2').repos.search('koko', mode='source')
# OR
        # search all repos

# Warning currently they produce same results (no idea why)

In [3]: repos = cl.repos.search('koko', mode='source')


In [4]: repos
Out[4]:
[
 <Repo: owned by current user: hamdy>
 {
     "id": 38,
     "clone_url": "http://172.17.0.2:3000/hamdy/koko.git",
     "description": "This repo is owner by user hamdy, the admin and the current gitea client user",
     "full_name": "hamdy/koko",
     "created_at": "2018-06-02T14:42:22Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.2:3000/hamdy/koko",
     "name": "koko",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.2:hamdy/koko.git"
 },
 <Repo>
 {
     "id": 35,
     "clone_url": "http://172.17.0.2:3000/hamdy2/koko.git",
     "full_name": "hamdy2/koko",
     "created_at": "2018-05-27T01:15:59Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.2:3000/hamdy2/koko",
     "name": "koko",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.2:hamdy2/koko.git"
 }]

In [6]: repos[0].user
Out[6]:

<Current User>
{
    "id": 1,
    "username": "hamdy",
    "password": null,
    "full_name": "",
    "login_name": null,
    "source_id": null,
    "send_notify": null,
    "email": "hamdy@greenitglobe.com",
    "active": null,
    "admin": null,
    "allow_git_hook": false,
    "allow_import_local": false,
    "location": null,
    "max_repo_creation": null,
    "website": null,
    "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"
}

In [7]: repos[1].user
Out[7]:

<User>
{
    "id": 90,
    "username": "hamdy2",
    "password": null,
    "full_name": "",
    "login_name": null,
    "source_id": null,
    "send_notify": null,
    "email": "jh@we.com",
    "active": null,
    "admin": null,
    "allow_git_hook": false,
    "allow_import_local": false,
    "location": null,
    "max_repo_creation": null,
    "website": null,
    "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon"
}

```

**Get repo by ID**

```
In [4]: cl.repos.get(38)
Out[4]:

<Repo: owned by current user: hamdy>
{
    "id": 38,
    "clone_url": "http://172.17.0.2:3000/hamdy/koko.git",
    "description": "This repo is owner by user hamdy, the admin and the current gitea client user",
    "full_name": "hamdy/koko",
    "created_at": "2018-06-02T14:42:22Z",
    "default_branch": "master",
    "empty": true,
    "html_url": "http://172.17.0.2:3000/hamdy/koko",
    "name": "koko",
    "owner": {
        "id": 1,
        "login": "hamdy",
        "full_name": "",
        "email": "hamdy@greenitglobe.com",
        "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
        "username": "hamdy"
    },
    "stars_count": 1,
    "watchers_count": 1,
    "ssh_url": "gitea@172.17.0.2:hamdy/koko.git"
}

In [5]: cl.repos.get(35)
Out[5]:

<Repo>
{
    "id": 35,
    "clone_url": "http://172.17.0.2:3000/hamdy2/koko.git",
    "full_name": "hamdy2/koko",
    "created_at": "2018-05-27T01:15:59Z",
    "default_branch": "master",
    "empty": true,
    "html_url": "http://172.17.0.2:3000/hamdy2/koko",
    "name": "koko",
    "owner": {
        "id": 90,
        "login": "hamdy2",
        "full_name": "",
        "email": "jh@we.com",
        "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
        "username": "hamdy2"
    },
    "watchers_count": 1,
    "ssh_url": "gitea@172.17.0.2:hamdy2/koko.git"
}

```

**User Repos**
```
In [3]: cl.users.current.repos
Out[3]: <Repos Iterator for user: hamdy>

In [7]: [r for r in cl.users.current.repos]
Out[7]:
[
 <Repo: owned by current user: hamdy>
 {
     "id": 38,
     "clone_url": "http://172.17.0.3:3000/hamdy/koko.git",
     "description": "This repo is owner by user hamdy, the admin and the current gitea client user",
     "full_name": "hamdy/koko",
     "created_at": "2018-06-02T14:42:22Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/koko",
     "name": "koko",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "stars_count": 1,
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/koko.git"
 },
 <Repo: owned by current user: hamdy>
 {
     "id": 37,
     "clone_url": "http://172.17.0.3:3000/hamdy/repoooo.git",
     "full_name": "hamdy/repoooo",
     "created_at": "2018-05-27T01:25:53Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/repoooo",
     "name": "repoooo",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "stars_count": 1,
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/repoooo.git"
 },
 <Repo: owned by current user: hamdy>
 {
     "id": 34,
     "clone_url": "http://172.17.0.3:3000/hamdy/soso.git",
     "full_name": "hamdy/soso",
     "created_at": "2018-05-27T01:12:47Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/soso",
     "name": "soso",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/soso.git"
 }]


# For another user

In [2]: u = cl.users.get('hamdy2')

In [3]: u.repos
Out[3]: <Repos Iterator for user: hamdy2>

In [4]: [a for a in u.repos]
Out[4]:
[
 <Repo>
 {
     "id": 36,
     "clone_url": "http://172.17.0.3:3000/hamdy2/lolo.git",
     "full_name": "hamdy2/lolo",
     "created_at": "2018-05-27T01:21:41Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/lolo",
     "name": "lolo",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/lolo.git"
 },
 <Repo>
 {
     "id": 35,
     "clone_url": "http://172.17.0.3:3000/hamdy2/koko.git",
     "full_name": "hamdy2/koko",
     "created_at": "2018-05-27T01:15:59Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/koko",
     "name": "koko",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/koko.git"
 }]
```

**Create repo for another user (requires admin permissions)**

```
In [2]: u = cl.users.get('hamdy2')
In [3]: repo = u.repos.new()
In [5]: repo.name = 'lolo'

In [6]: repo.save()
[Sat02 15:49] - GiteaRepo.py      :176 :j.gitearepoforowner  - ERROR    - b'{"message":"repository already exists [uname: hamdy2, name: lolo]","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}'
Out[6]: False

In [7]: repo.name = 'dodo'

In [8]: repo.save()
Out[8]: True


# create repo for current user (no admin permissions required)

In [9]: repo = cl.users.current.repos.new()

In [10]: repo.name = 'repoooo'

In [11]: repo.save()
[Sat02 15:50] - GiteaRepo.py      :176 :j.gitearepoforowner  - ERROR    - b'{"message":"repository already exists [uname: hamdy, name: repoooo]","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}'
Out[11]: False

In [12]: repo.name = 'new'

In [13]: repo.save()
Out[13]: True

```

**Starring**

```
In [3]: hamdy2 = cl.users.get('hamdy2')

In [4]: curr = cl.users.current

In [5]: curr.repos.starred
Out[5]: []

In [6]: repo = hamdy2.repos.get('dodo')

In [7]: repo.is_starred_by_current_user
Out[7]: False

In [8]: repo.unstar()
Out[8]: True

In [9]: repo.star()
Out[9]: True

In [10]: repo.star()
Out[10]: True

In [11]: repo.is_starred_by_current_user()
Out[11]: True

In [12]: curr.repos.stared
Out[12]:
[
 <Repo>
 {
     "id": 39,
     "clone_url": "http://172.17.0.3:3000/hamdy2/dodo.git",
     "full_name": "hamdy2/dodo",
     "created_at": "2018-06-02T15:49:17Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/dodo",
     "name": "dodo",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "stars_count": 1,
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/dodo.git"
 }]
```

**Subscriptions**

```
In [13]: curr.repos.subscriptions
Out[13]:
[
 <Repo: owned by current user: hamdy>
 {
     "id": 34,
     "clone_url": "http://172.17.0.3:3000/hamdy/soso.git",
     "full_name": "hamdy/soso",
     "created_at": "2018-05-27T01:12:47Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/soso",
     "name": "soso",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/soso.git"
 },
 <Repo>
 {
     "id": 35,
     "clone_url": "http://172.17.0.3:3000/hamdy2/koko.git",
     "full_name": "hamdy2/koko",
     "created_at": "2018-05-27T01:15:59Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/koko",
     "name": "koko",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/koko.git"
 },
 <Repo>
 {
     "id": 36,
     "clone_url": "http://172.17.0.3:3000/hamdy2/lolo.git",
     "full_name": "hamdy2/lolo",
     "created_at": "2018-05-27T01:21:41Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/lolo",
     "name": "lolo",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/lolo.git"
 },
 <Repo: owned by current user: hamdy>
 {
     "id": 37,
     "clone_url": "http://172.17.0.3:3000/hamdy/repoooo.git",
     "full_name": "hamdy/repoooo",
     "created_at": "2018-05-27T01:25:53Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/repoooo",
     "name": "repoooo",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/repoooo.git"
 },
 <Repo: owned by current user: hamdy>
 {
     "id": 38,
     "clone_url": "http://172.17.0.3:3000/hamdy/koko.git",
     "description": "This repo is owner by user hamdy, the admin and the current gitea client user",
     "full_name": "hamdy/koko",
     "created_at": "2018-06-02T14:42:22Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/koko",
     "name": "koko",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/koko.git"
 },
 <Repo>
 {
     "id": 39,
     "clone_url": "http://172.17.0.3:3000/hamdy2/dodo.git",
     "full_name": "hamdy2/dodo",
     "created_at": "2018-06-02T15:49:17Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy2/dodo",
     "name": "dodo",
     "owner": {
         "id": 90,
         "login": "hamdy2",
         "full_name": "",
         "email": "jh@we.com",
         "avatar_url": "https://secure.gravatar.com/avatar/f08f0fa33c500694089a0359f3692490?d=identicon",
         "username": "hamdy2"
     },
     "stars_count": 1,
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy2/dodo.git"
 },
 <Repo: owned by current user: hamdy>
 {
     "id": 40,
     "clone_url": "http://172.17.0.3:3000/hamdy/new.git",
     "full_name": "hamdy/new",
     "created_at": "2018-06-02T15:50:32Z",
     "default_branch": "master",
     "empty": true,
     "html_url": "http://172.17.0.3:3000/hamdy/new",
     "name": "new",
     "owner": {
         "id": 1,
         "login": "hamdy",
         "full_name": "",
         "email": "hamdy@greenitglobe.com",
         "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
         "username": "hamdy"
     },
     "watchers_count": 1,
     "ssh_url": "gitea@172.17.0.3:hamdy/new.git"
 }]
```


**Repo Migrations**

```
In [14]: curr.repos.migrate('hamdy', 'my-secret', 'https://github.com/hamdy/knn', 'knn')
Out[14]:

<Repo: owned by current user: hamdy>
{
    "id": 41,
    "clone_url": "http://172.17.0.3:3000/hamdy/knn.git",
    "full_name": "hamdy/knn",
    "created_at": "0001-01-01T00:00:00Z",
    "default_branch": "master",
    "html_url": "http://172.17.0.3:3000/hamdy/knn",
    "mirror": true,
    "name": "knn",
    "owner": {
        "id": 1,
        "login": "hamdy",
        "full_name": "",
        "email": "hamdy@greenitglobe.com",
        "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon",
        "username": "hamdy"
    },
    "size": 28,
    "watchers_count": 1,
    "ssh_url": "gitea@172.17.0.3:hamdy/knn.git"
}

```

**Repo Download**

```
In [2]: curr = cl.users.current

In [3]: knn = curr.repos.get('knn')

In [4]: knn.download(dir='/tmp/knn', type='tar.gz')
Out[4]: True

In [5]: knn.download(dir='/tmp/knn', branch='master', type='tar.gz')
Out[5]: True

In [6]: knn.download(dir='/tmp/knn', branch='master', type='zip')
Out[6]: True

In [7]: knn.download(dir='/tmp/knn') # master.zip
Out[7]: True
```

**Download single file**
```
In [2]: curr = cl.users.current

In [3]: knn = curr.repos.get('knn')

In [4]: knn.download_file(destination_dir='/tmp/downloads', filename='knn.py', branch='master')
Out[4]: True

In [5]: knn.download_file(destination_dir='/tmp/downloads', filename='knn.py') # download from master
   ...:
Out[5]: True

```

--


```python
# organizations

# for current user
In [2]: ham = cl.users.get('hamdy')

In [3]: ham.organizations
Out[3]: Gitea Organizations Iterator for user: hamdy

In [9]: [x for x in ham.organizations]
Out[9]:
[{"id": 87, "avatar_url": "http://172.17.0.2:3000/avatars/87", "username": "gigaya"},
 {"id": 88, "avatar_url": "http://172.17.0.2:3000/avatars/88", "username": "ss"}]

# for another user
In [10]: u = cl.users.get('ooo')

In [11]: [x for x in u.organizations]
Out[11]: []

# org hooks


In [1]: cl = j.clients.gitea.get()
In [7]: [h for h in x.hooks]
[Web hook {"id": 3, "created_at": "2018-05-13T00:16:34Z", "updated_at": "2018-05-13T00:16:34Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://kk.com", "config": {"url": "http://kk.com", "content_type": "json"}},
 Web hook {"id": 4, "created_at": "2018-05-13T00:26:37Z", "updated_at": "2018-05-13T00:26:37Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 5, "created_at": "2018-05-13T00:27:29Z", "updated_at": "2018-05-13T00:27:29Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 6, "created_at": "2018-05-13T00:28:34Z", "updated_at": "2018-05-13T00:28:34Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 7, "created_at": "2018-05-13T00:31:33Z", "updated_at": "2018-05-13T00:31:33Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 8, "created_at": "2018-05-13T00:33:31Z", "updated_at": "2018-05-13T00:33:31Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://ff.com", "config": {"url": "http://ff.com", "content_type": "json"}},
 Web hook {"id": 9, "created_at": "2018-05-13T00:34:56Z", "updated_at": "2018-05-13T00:34:56Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 10, "created_at": "2018-05-13T00:36:11Z", "updated_at": "2018-05-13T00:36:11Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}},
 Web hook {"id": 11, "created_at": "2018-05-13T00:38:06Z", "updated_at": "2018-05-13T00:38:06Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://sd.com", "config": {"url": "http://sd.com", "content_type": "json"}}]


In [9]: h = x.hooks.new()
In [11]: h.url = 'http://sd.com'
In [12]: h.type  = 'gitea'
In [14]: h.events=['push']
In [15]: h.save()
Out[15]: (True, '')
In [16]: h.update()
Out[16]: (True, '')
In [18]: h.delete()
Out[18]: (True, '')


# org members
cl = j.clients.gitea.get()
In [2]: x = cl.organizations.get('gigaya', fetch=True)
In [3]: x.members
Out[3]: Gitea Members Iterator for organization: gigaya

In [4]: [x for x in x.members]
Out[4]: [{"id": 1, "username": "hamdy", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"}]

In [23]: x.members.unregister(username='hamdy')
Out[23]:
(False,
 b'{"message":"user is the last member of owner team [uid: 1]","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}')


In [24]: x.members.unregister(username='ha')
Out[24]: (False, b'Not found')

# assuming user ooo belongs to a team in the organization
In [25]: x.members.unregister(username='ooo')
Out[25]: (True, '')


In [2]: x=cl.organizations.get('kk', fetch=True)

In [3]: x.members.public
Out[3]: []

In [4]: x.members.publicize('hamdy')
Out[4]: True

In [5]: x.members.public
Out[5]: [{"id": 1, "username": "hamdy", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"}]

In [6]: x.members.conceal('hamdy')
Out[6]: True

In [7]: x.members.public
Out[7]: []

In [8]: x.members.is_public('hamdy')
Out[8]: False

# teams
In [2]: x = cl.organizations.get('gigaya', fetch=True)

In [3]: t = x.teams.new()

In [4]: t.name = 'ee'

In [5]: t.save()
Out[5]:
(False,
 b'{"message":"team already exists [org_id: 87, name: ee]","url":"https://godoc.org/github.com/go-gitea/go-sdk/gitea"}')

In [6]: t.name = 'eeee'

In [6]: t.save()
Out[6]: (False, 'create Error {"permission": "Missing"}')

In [7]: t.permission = 'ss'

In [8]: t.save()
Out[8]:
(False,
 'create Error {"permission": "Only allowed [owner, admin, read, write]"}')

In [9]: t.permission = 'admin'

In [10]: t.save()
Out[10]: (True, '')


In [8]: t.update()
Out[8]: (True, '')

In [9]: t.delete()
Out[9]: (True, '')

# --

In [2]: x=cl.organizations.get('kk', fetch=True)

In [5]: t = x.teams.get(id=11)

In [6]: t
Out[6]: <Team> {"id": 11, "description": null, "name": null, "permission": null}

In [7]: t.members
Out[7]: Gitea Members Iterator for team: 11

In [8]: [m for m in t.members]
Out[8]: [{"id": 1, "username": "hamdy", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"}]


In [2]: x = cl.organizations.get('gigaya', fetch=True)

In [3]: t = x.teams.get(id=12)

In [4]: t.members.add('ooo')
Out[4]: (True, '')

In [5]: [a for a in t.members]
Out[5]:
[{"id": 1, "username": "hamdy", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"},
 {"id": 84, "username": "ooo", "email": "ham@ham.com", "avatar_url": "https://secure.gravatar.com/avatar/547302594c1f80a224bf0638d04edfe3?d=identicon"}]

In [4]: t.members.remove('ooo')
Out[4]: (True, '')

In [5]: [a for a in t.members]
Out[5]: [{"id": 1, "username": "hamdy", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon"}]

# Repos

In [4]: cl.repos.get_by_id(30)
Out[4]: {"id": 30, "clone_url": "http://172.17.0.2:3000/hamdy/crm.git", "full_name": "hamdy/crm", "created_at": "2018-05-21T01:15:02Z", "default_branch": "master", "html_url": "http://172.17.0.2:3000/hamdy/crm", "mirror": true, "name": "crm", "owner": {"id": 1, "login": "hamdy", "full_name": "", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon", "username": "hamdy"}, "size": 28, "watchers_count": 1, "ssh_url": "gitea@172.17.0.2:hamdy/crm.git"}


r = cl.repos.migrate(clone_addr='https://github.com/hamdy/knn', auth_password='sfafefewfwef', auth_username='hamdy', repo_name='crm', uid=1)
{'id': 27, 'owner': {'id': 1, 'login': 'hamdy', 'full_name': '', 'email': 'hamdy@greenitglobe.com', 'avatar_url': 'https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon', 'username': 'hamdy'}, 'name': 'crm', 'full_name': 'hamdy/crm', 'description': '', 'empty': False, 'private': True, 'fork': False, 'parent': None, 'mirror': True, 'size': 28, 'html_url': 'http://172.17.0.2:3000/hamdy/crm', 'ssh_url': 'gitea@172.17.0.2:hamdy/crm.git', 'clone_url': 'http://172.17.0.2:3000/hamdy/crm.git', 'website': '', 'stars_count': 0, 'forks_count': 0, 'watchers_count': 1, 'open_issues_count': 0, 'default_branch': 'master', 'created_at': '0001-01-01T00:00:00Z', 'updated_at': '0001-01-01T00:00:00Z', 'permissions': {'admin': True, 'push': True, 'pull': True}}

x = cl.repos.get(owner='hamdy', repo='crm', fetch=True)
Out[3]: {"id": 27, "clone_url": "http://172.17.0.2:3000/hamdy/crm.git", "full_name": "hamdy/crm", "created_at": "2018-05-19T14:55:15Z", "default_branch": "master", "html_url": "http://172.17.0.2:3000/hamdy/crm", "mirror": true, "name": "crm", "owner": {"id": 1, "login": "hamdy", "full_name": "", "email": "hamdy@greenitglobe.com", "avatar_url": "https://secure.gravatar.com/avatar/859fe0c48f17055d3893ebd4fb218b91?d=identicon", "username": "hamdy"}, "size": 28, "watchers_count": 1, "ssh_url": "gitea@172.17.0.2:hamdy/crm.git"}

x = cl.repos.get(owner='hamdy', repo='toto', fetch=False)
x.delete()
(True, '')

    # Branches
In [2]: x = cl.repos.get(owner='hamdy', repo='crm')

In [3]: [a for a in x.branches]
Out[3]: [Branch <{"id": null, "name": "master", "commit": {"id": "31dedf15579c31596911ac66aaf48abf0bd12c7a", "message": "Knn algorithm baic implementation and test\n", "url": "Not implemented", "author": {"name": "Hamdy", "email": "hamdy.a.farag@gmail.com", "username": ""}, "committer": {"name": "Hamdy", "email": "hamdy.a.farag@gmail.com", "username": ""}, "verification": {"verified": false, "reason": "gpg.error.not_signed_commit", "signature": "", "payload": ""}, "timestamp": "2016-01-23T19:46:26Z"}, "committer": null, "message": null, "timestamp": null, "verification": null, "url": null}>]

In [4]: x.branches.get(name='master')
Out[4]: Branch <{"id": null, "name": null, "commit": null, "committer": null, "message": null, "timestamp": null, "verification": null, "url": null}>

In [5]: x.branches.get(name='master', fetch=True)
Out[5]: Branch <{"id": null, "name": "master", "commit": {"id": "31dedf15579c31596911ac66aaf48abf0bd12c7a", "message": "Knn algorithm baic implementation and test\n", "url": "Not implemented", "author": {"name": "Hamdy", "email": "hamdy.a.farag@gmail.com", "username": ""}, "committer": {"name": "Hamdy", "email": "hamdy.a.farag@gmail.com", "username": ""}, "verification": {"verified": false, "reason": "gpg.error.not_signed_commit", "signature": "", "payload": ""}, "timestamp": "2016-01-23T19:46:26Z"}, "committer": null, "message": null, "timestamp": null, "verification": null, "url": null}>

    # collaborators
In [2]: x = cl.repos.get(owner='hamdy', repo='crm')

In [3]: x.collaborators.is_collaborator('ooos')
Out[3]: False

In [4]: x.collaborators.is_collaborator('ooo')
Out[4]: True

In [5]: x.collaborators.remove('ooo')
Out[5]: (True, '')

In [6]: x.collaborators.is_collaborator('ooo')
Out[6]: False

In [7]: x.collaborators.add('ooo')
Out[7]: (True, '')

In [8]: x.collaborators.remove('ooo')
Out[8]: True

In [9]: x.collaborators.is_collaborator('ooo')
Out[9]: False


    # Repo Hooks

x = cl.repos.get(owner='hamdy', repo='crm')
In [3]: [h for h in x.hooks]
Out[4]: [Web hook {"id": 15, "created_at": "2018-05-21T09:52:20Z", "updated_at": "2018-05-21T09:52:20Z", "active": true, "events": ["push"], "type": "gitea", "content_type": "json", "url": "http://dd.com", "config": {"url": "http://dd.com", "content_type": "json"}}]

n [2]: x = cl.repos.get(owner='hamdy', repo='crm')

In [3]: h = x.hooks.new()

In [4]: h.type  = 'gitea'

In [5]: h.url = 'http://sd.com'

In [6]: h.events=['push']

In [7]: h.save()
Out[7]: (True, '')

In [8]: h.update()
Out[8]: (True, '')

    # Repo Keys

In [2]: x = cl.repos.get(owner='hamdy', repo='crm')

In [3]: x.keys
Out[3]: PublicKeys Iterator for repo: crm

In [4]: [a for a in x.keys]
Out[4]: []

In [5]: k = x.keys.new()

In [6]: k.key = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoxqC1QNqEJculbDP7wRI3PRtn6yoNo52HbYty9swIjg
   ...: 1OqdrDstgw0FKwe9OBYjZpYXCPnyieQ4d3O26Xc4Rc+w88diJKPanlDZV5BpOvbu0NwvAJbxhqz1Ca25KETllBhH30HMl
   ...: yZGoc2uFWZpw8y9zNFl384TBWLwMD3aUQ2XejVdZxCC7u3CTZU6sQgKipk76t9USgyKpRLkanUUV2OV3WIeLbA4/zr71Q
   ...: u9IEaxNMLPD3JBZummcERJjJksHbOdybXiEqGMDeSDj5WGxulsVwYhBaTOUxeuf9UErKh/H2HuyCxSj8JaihHNgyiV5gw
   ...: JNED9fo/ktqk4rb43np root@js"""

In [7]: k.title = "new_key"

In [8]: k.save()
Out[8]: (True, '')

In [9]: [a for a in x.keys]
Out[9]: [{"id": 1, "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoxqC1QNqEJculbDP7wRI3PRtn6yoNo52HbYty9swIjg1OqdrDstgw0FKwe9OBYjZpYXCPnyieQ4d3O26Xc4Rc+w88diJKPanlDZV5BpOvbu0NwvAJbxhqz1Ca25KETllBhH30HMlyZGoc2uFWZpw8y9zNFl384TBWLwMD3aUQ2XejVdZxCC7u3CTZU6sQgKipk76t9USgyKpRLkanUUV2OV3WIeLbA4/zr71Qu9IEaxNMLPD3JBZummcERJjJksHbOdybXiEqGMDeSDj5WGxulsVwYhBaTOUxeuf9UErKh/H2HuyCxSj8JaihHNgyiV5gwJNED9fo/ktqk4rb43np root@js", "title": "new_key", "created_at": "2018-05-21T10:17:51Z", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/crm/keys/1"}]
In [4]: k.delete()
Out[4]: (True, '')

In [5]: [a for a in x.keys]
Out[5]: []

In [2]: x = cl.repos.get(owner='hamdy2', repo='repo', fetch=True)

In [3]: pr = x.pull_requests.get(1, fetch=True)

In [4]: pr = x.pull_requests.get(2, fetch=True)

In [5]: pr.merged
Out[5]: False

In [6]: pr.merge()
Out[6]: True

# Get raw file
In [9]: x = cl.repos.get(owner='hamdy', repo='crm')
In [9]: x.get_file('master/knn.py')

    # issues
n [2]: x = cl.repos.get(owner='hamdy', repo='koko')

In [3]: issue = x.issues.new()

In [4]: issue.title = 'ui'

In [5]: issue.body = 'ui'

In [6]: issue.save()
Out[6]: (True, '')

In [7]: issue.id
Out[7]: 3

In [8]: issue.title = 'ui ui '

In [9]: issue.update()
Out[9]: (True, '')

In [2]: x = cl.repos.get(owner='hamdy', repo='koko')

In [3]: [a for a in x.issues]
Out[3]:
[{"id": 4, "assignee": null, "assignees": [], "body": "scsc", "due_date": null, "labels": [], "milestone": null, "title": "sdsd", "state": "open", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/koko/issues/17", "updated_at": "2018-05-22T12:03:59Z"},
 {"id": 2, "assignee": null, "assignees": [], "body": "rt", "due_date": null, "labels": [], "milestone": null, "title": "rt", "state": "open", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/koko/issues/15", "updated_at": "2018-05-22T11:19:24Z"},
 {"id": 1, "assignee": null, "assignees": [], "body": "rt", "due_date": null, "labels": [], "milestone": null, "title": "rt", "state": "open", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/koko/issues/14", "updated_at": "2018-05-22T11:18:40Z"}]

In [4]: x.issues.list(page=1, state='closed')
Out[4]: [{"id": 3, "assignee": null, "assignees": [], "body": "ui", "due_date": null, "labels": [], "milestone": null, "title": "ui ui ", "state": "closed", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/koko/issues/16", "updated_at": "2018-05-22T11:39:13Z"}]


In [6]: x.issues.get('3', fetch=True)
Out[6]: {"id": 3, "assignee": null, "assignees": [], "body": "ui", "due_date": null, "labels": [], "milestone": null, "title": "ui ui ", "state": "closed", "url": "http://172.17.0.2:3000/api/v1/repos/hamdy/koko/issues/16", "updated_at": "2018-05-22T11:39:13Z"}

In [7]: i = x.issues.get('3', fetch=True)

In [8]: i.title = 'yy'

In [9]: i.update()
Out[9]: (True, '')

# issue commnets
In [2]: x = cl.repos.get(owner='hamdy', repo='koko')

In [3]: i = x.issues.get('3', fetch=True)

In [4]: [c for c in i.issue_comments][0]
Out[4]: Comment {"id": 23, "created_at": "2018-05-23T08:55:11Z", "pull_request_url": "", "html_url": "http://172.17.0.2:3000/hamdy/koko/issues/3#issuecomment-23", "body": "asascsac"}

In [5]: [c for c in i.issue_comments]
Out[5]: [Comment {"id": 23, "created_at": "2018-05-23T08:55:11Z", "pull_request_url": "", "html_url": "http://172.17.0.2:3000/hamdy/koko/issues/3#issuecomment-23", "body": "asascsac"}]

In [2]: x = cl.repos.get(owner='hamdy', repo='koko')

In [3]: i = x.issues.get('3', fetch=True)

In [4]: ii = i.issue_comments.new()

In [5]: ii.body = 'niahaha'

In [6]: ii.save()
Out[6]: (True, '')

In [7]: ii.body = 'niaaaaaaaaaaaaaaaaaaaaaaah'

In [8]: ii.update()
Out[8]: (True, '')

In [9]: ii.delete()
Out[10]: (True, '')

# repo milestones
In [2]: x = cl.repos.get(owner='hamdy', repo='koko')

In [3]: [m for m in x.milestones]
Out[3]:
[Milestone {"id": 196, "closed_at": null, "closed_issues": 0, "description": "kjjhhhhhhhh", "due_on": null, "open_issues": 0, "title": "milaya"},
 Milestone {"id": 197, "closed_at": null, "closed_issues": 0, "description": "", "due_on": null, "open_issues": 0, "title": "lll"}]

In [4]: ms = x.milestones.new()

In [5]: ms.title = 'aaaa'

In [6]: ms.save()
Out[6]: (True, '')

In [7]: ms.title = 'bbb'

In [8]: ms.update()
Out[8]: (True, '')

In [9]: ms.delete()
Out[9]: (True, '')

# repo labels

In [17]: x = cl.repos.get(owner='hamdy', repo='koko')

In [18]: [a for a in x.labels]
Out[18]:
[Label {"id": 125, "name": "bug", "color": "ee0701"},
 Label {"id": 126, "name": "duplicate", "color": "cccccc"},
 Label {"id": 127, "name": "enhancement", "color": "84b6eb"},
 Label {"id": 128, "name": "help wanted", "color": "128a0c"},
 Label {"id": 129, "name": "invalid", "color": "e6e6e6"},
 Label {"id": 130, "name": "question", "color": "cc317c"},
 Label {"id": 131, "name": "wontfix", "color": "ffffff"}]


In [5]: label = x.labels.new()
In [27]: label.name = 'label'
In [30]: label.color = '#244d12'

In [31]: label.save()
Out[31]: (True, '')

In [32]: label.update()
Out[32]: (True, '')

In [33]: label.delete()
Out[33]: (True, '')

In [35]: x.labels.get('125', fetch=True)
Out[35]: Label {"id": 125, "name": "bug", "color": "ee0701"}

```

