#coding=utf-8
import redis
import time
redis_from = redis.StrictRedis(host='192.168.1.1', port=6380, db=4)
redis_to = redis.StrictRedis(host='127.0.0.1', port=6380, db=4)
if __name__ == '__main__':
    cnt = 0
    star_time = time.asctime( time.localtime(time.time()))
    for k in redis_from.keys():
        data_type = redis_from.type(k)
        #print(type(data_type))
        data_type = data_type.decode()
        #print(type(data_type))
        if data_type == 'string':
            v = redis_from.get(k)
            redis_to.set(k, v)
        elif data_type == 'list':
            values = redis_from.lrange(k, 0, -1)
            redis_to.lpush(k, values)
        elif data_type == 'set':
            values = redis_from.smembers(k)
            redis_to.sadd(k, values)
        elif data_type == 'hash':
            keys = redis_from.hkeys(k)
            for key in keys:
                value = redis_from.hget(k, key)
                redis_to.hset(k, key, value)
        else:
            print('not known type', data_type)
        cnt = cnt + 1
    end_time = time.asctime(time.localtime(time.time()))
    print('total', cnt, "开始时间：{} \n 结束时间为：{}".format(star_time, end_time))
