from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb+srv://dhwani_02:dhwani_02@cluster0.fy6bc1b.mongodb.net/")
db = client['ytmanager']
video_collection = db["videos"]
print(video_collection)


def add_video(name, time):
  video_collection.insert_one({"name":name, "time": time})


def list_video():
  for video in video_collection.find():
    print(f"Id: {video['_id']}, Name: {video['name']} and Time: {video['time']}")


def update_video(video_id, new_name, new_time):
  video_collection.update_one(
    {'_id': ObjectId(video_id)}, 
    {"$set": {"name": new_name, "time": new_time}}
  )

def delete_video(video_id):
  video_collection.delete_one({"_id":video_id})


def main():
  while True:
    print("\n Youtube Manager App")
    print("1. List all videos")
    print("2. Add a new videos")
    print("3. Update a videos")
    print("4. Delete a videos")
    print("5. Exit")

    choice = input("Enter your choice : ")

    if choice == '1':
      list_video()
      
    elif choice == '2':
      name = input("Enter the video name : ")
      time = input("Enter the video time : ")
      add_video(name, time)

    elif choice == '3':
      video_id = input("Enter the video id to update : ")
      name = input("Enter the updated video name : ")
      time = input("Enter the updated video time : ")
      update_video(video_id, name, time)

    elif choice == '4':
        video_id = input("Enter the video id to delete : ")
        delete_video(video_id)

    elif choice == '5':
      break

    else:
      print("Enter valid choice")


if __name__ == "__main__":
  main()

