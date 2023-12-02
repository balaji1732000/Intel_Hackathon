# #k = r8_TfvDehGo5PSsfcaWynCXJPfukI2XyYJ22KBuR
import replicate
# output = replicate.run(
#     "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
#     input={"image": open("Screenshot 2023-05-31.png", "rb")}
# )

# print(output)
# # The yorickvp/llava-13b model can stream output as it's running.
# # The predict method returns an iterator, and you can iterate over that output.
# for item in output:
#     # https://replicate.com/yorickvp/llava-13b/versions/e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358/api#output-schema
#     print(item, end="")


output = replicate.run(
  "yorickvp/llava-13b:c293ca6d551ce5e74893ab153c61380f5bcbd80e02d49e08c582de184a8f6c83",
  input={
    "image": "https://replicate.delivery/pbxt/JfvBi04QfleIeJ3ASiBEMbJvhTQKWKLjKaajEbuhO1Y0wPHd/view.jpg",
    "prompt": "what is in this picture",
    "max_tokens": 1024,
    "temperature": 0.2
  }
)
print(output)